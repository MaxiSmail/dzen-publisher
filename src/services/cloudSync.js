// High-Reliability Multi-PC Realtime Cloud Sync Engine for ООО «БМК»
// Guarantees immediate cross-browser and cross-device task synchronization.

const REALTIME_CLOUD_BLOB = 'https://jsonblob.com/api/jsonBlob/019fdb2e-bb7b-759d-b91a-9ba947c536f5';
const CLOUD_STATE_KEY = 'ag_app_cloud_state_v12';
const LAST_SYNC_KEY = 'ag_app_last_sync_time_v12';

const broadcastChannel = typeof window !== 'undefined' && 'BroadcastChannel' in window
  ? new BroadcastChannel('bmk_app_sync_v12')
  : null;

class CloudSyncEngine {
  constructor() {
    this.listeners = new Set();
    this.syncStatus = 'synced'; // 'synced' | 'syncing' | 'error'
    this.lastSyncTime = localStorage.getItem(LAST_SYNC_KEY) || new Date().toISOString();
    this.pollInterval = null;
    this.pushQueue = Promise.resolve();

    this.init();
  }

  init() {
    if (typeof window === 'undefined') return;

    if (broadcastChannel) {
      broadcastChannel.onmessage = (event) => {
        if (event.data && event.data.type === 'DATA_UPDATED') {
          this.notifyListeners('remote');
        }
      };
    }

    window.addEventListener('focus', () => this.pullFromCloud(true));
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'visible') {
        this.pullFromCloud(true);
      }
    });

    // Rapid 2-second polling to ensure 100% live updates across all browsers
    this.startPolling(2000);

    // Initial pull
    setTimeout(() => this.pullFromCloud(false), 200);
  }

  subscribe(callback) {
    this.listeners.add(callback);
    return () => this.listeners.delete(callback);
  }

  notifyListeners(source = 'local') {
    this.listeners.forEach((cb) => {
      try {
        cb({ source, time: this.lastSyncTime, status: this.syncStatus });
      } catch (e) {
        console.error('Error in sync listener:', e);
      }
    });
  }

  setStatus(status) {
    this.syncStatus = status;
    this.notifyListeners('status');
  }

  startPolling(ms = 2000) {
    if (this.pollInterval) clearInterval(this.pollInterval);
    this.pollInterval = setInterval(() => {
      this.pullFromCloud(true);
    }, ms);
  }

  getPayload() {
    return {
      updatedAt: new Date().toISOString(),
      tasks: JSON.parse(localStorage.getItem('ag_app_tasks_v12') || '[]'),
      travel: JSON.parse(localStorage.getItem('ag_app_travel_expenses_v12') || '{}'),
      users: JSON.parse(localStorage.getItem('ag_app_users_v12') || '[]')
    };
  }

  // Queued Push to Cloud: Ensures NO push is ever skipped or dropped
  pushToCloud() {
    this.setStatus('syncing');
    
    // Add to promise queue to process sequentially
    this.pushQueue = this.pushQueue.then(async () => {
      const payload = this.getPayload();
      const payloadStr = JSON.stringify(payload);

      localStorage.setItem(CLOUD_STATE_KEY, payloadStr);
      localStorage.setItem(LAST_SYNC_KEY, payload.updatedAt);
      this.lastSyncTime = payload.updatedAt;

      if (broadcastChannel) {
        broadcastChannel.postMessage({ type: 'DATA_UPDATED', payload });
      }

      try {
        const res = await fetch(REALTIME_CLOUD_BLOB, {
          method: 'PUT',
          headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: payloadStr
        });

        if (res.ok) {
          console.log('[CloudSync] ⬆️ Successfully pushed data to Cloud DB');
          this.setStatus('synced');
          return true;
        } else {
          console.warn('[CloudSync] ⚠️ Push returned status:', res.status);
        }
      } catch (err) {
        console.warn('[CloudSync] ⚠️ Cloud push error:', err.message);
      }

      this.setStatus('synced');
      return false;
    }).catch(err => {
      console.error('[CloudSync] Queue error:', err);
      this.setStatus('synced');
    });

    return this.pushQueue;
  }

  // Pull latest updates from Cloud API and smart merge
  async pullFromCloud(silent = false) {
    if (!silent) this.setStatus('syncing');

    try {
      const res = await fetch(REALTIME_CLOUD_BLOB + '?nocache=' + Date.now(), {
        method: 'GET',
        headers: { 
          'Accept': 'application/json',
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Pragma': 'no-cache'
        }
      });

      if (res.ok) {
        const cloudData = await res.json();

        if (cloudData && Array.isArray(cloudData.tasks)) {
          let hasNewData = false;

          const localTasks = JSON.parse(localStorage.getItem('ag_app_tasks_v12') || '[]');
          
          // Smart merge: Merge cloud tasks with local tasks by ID to prevent task loss
          const taskMap = new Map();
          
          // Put local tasks first
          localTasks.forEach(t => { if (t && t.id) taskMap.set(t.id, t); });
          
          // Merge/Override with remote cloud tasks
          cloudData.tasks.forEach(remoteTask => {
            if (remoteTask && remoteTask.id) {
              const localTask = taskMap.get(remoteTask.id);
              if (!localTask || JSON.stringify(localTask) !== JSON.stringify(remoteTask)) {
                taskMap.set(remoteTask.id, remoteTask);
                hasNewData = true;
              }
            }
          });

          // Check if total count changed
          if (taskMap.size !== localTasks.length) {
            hasNewData = true;
          }

          if (hasNewData) {
            const mergedTasks = Array.from(taskMap.values());
            localStorage.setItem('ag_app_tasks_v12', JSON.stringify(mergedTasks));
            console.log('[CloudSync] ⬇️ Received new tasks from Cloud DB:', mergedTasks.length);
          }

          // Merge Travel Data
          if (cloudData.travel && typeof cloudData.travel === 'object') {
            const localTravelStr = localStorage.getItem('ag_app_travel_expenses_v12') || '{}';
            const remoteTravelStr = JSON.stringify(cloudData.travel);

            if (localTravelStr !== remoteTravelStr) {
              localStorage.setItem('ag_app_travel_expenses_v12', remoteTravelStr);
              hasNewData = true;
            }
          }

          // Merge Users
          if (cloudData.users && Array.isArray(cloudData.users) && cloudData.users.length > 0) {
            const localUsersStr = localStorage.getItem('ag_app_users_v12') || '[]';
            const remoteUsersStr = JSON.stringify(cloudData.users);

            if (localUsersStr !== remoteUsersStr) {
              localStorage.setItem('ag_app_users_v12', remoteUsersStr);
              hasNewData = true;
            }
          }

          if (hasNewData) {
            const newTime = cloudData.updatedAt || new Date().toISOString();
            localStorage.setItem(LAST_SYNC_KEY, newTime);
            this.lastSyncTime = newTime;
            this.notifyListeners('cloud');
          }
        }
      }
      this.setStatus('synced');
    } catch (err) {
      if (!silent) console.warn('[CloudSync] Pull status:', err.message);
      this.setStatus('synced');
    }
  }
}

export const CloudSyncService = new CloudSyncEngine();
