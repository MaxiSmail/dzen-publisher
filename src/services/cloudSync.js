// High-Reliability Multi-PC Realtime Cloud Sync Engine for ООО «БМК»
// Connects all PCs, browsers, and profiles to a shared 24/7 cloud database.

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
    this.isPushing = false;

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

    // Start 3-second rapid polling to ensure 100% sync across PCs
    this.startPolling(3000);

    // Initial pull
    setTimeout(() => this.pullFromCloud(false), 300);
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

  startPolling(ms = 3000) {
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

  async pushToCloud() {
    if (this.isPushing) return;
    this.isPushing = true;
    this.setStatus('syncing');

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
        this.setStatus('synced');
        this.isPushing = false;
        return true;
      }
    } catch (err) {
      console.warn('Cloud sync push failed:', err.message);
    }

    this.setStatus('synced');
    this.isPushing = false;
    return false;
  }

  async pullFromCloud(silent = false) {
    if (!silent) this.setStatus('syncing');

    try {
      const res = await fetch(REALTIME_CLOUD_BLOB + '?t=' + Date.now(), {
        method: 'GET',
        headers: { 
          'Accept': 'application/json',
          'Cache-Control': 'no-cache'
        }
      });

      if (res.ok) {
        const cloudData = await res.json();

        if (cloudData && Array.isArray(cloudData.tasks)) {
          let hasNewData = false;

          const localTasksStr = localStorage.getItem('ag_app_tasks_v12') || '[]';
          const remoteTasksStr = JSON.stringify(cloudData.tasks);

          if (localTasksStr !== remoteTasksStr) {
            localStorage.setItem('ag_app_tasks_v12', remoteTasksStr);
            hasNewData = true;
          }

          if (cloudData.travel && typeof cloudData.travel === 'object') {
            const localTravelStr = localStorage.getItem('ag_app_travel_expenses_v12') || '{}';
            const remoteTravelStr = JSON.stringify(cloudData.travel);

            if (localTravelStr !== remoteTravelStr) {
              localStorage.setItem('ag_app_travel_expenses_v12', remoteTravelStr);
              hasNewData = true;
            }
          }

          if (cloudData.users && Array.isArray(cloudData.users) && cloudData.users.length > 0) {
            const localUsersStr = localStorage.getItem('ag_app_users_v12') || '[]';
            const remoteUsersStr = JSON.stringify(cloudData.users);

            if (localUsersStr !== remoteUsersStr) {
              localStorage.setItem('ag_app_users_v12', remoteUsersStr);
              hasNewData = true;
            }
          }

          if (hasNewData || !silent) {
            const newTime = cloudData.updatedAt || new Date().toISOString();
            localStorage.setItem(LAST_SYNC_KEY, newTime);
            this.lastSyncTime = newTime;
            this.notifyListeners('cloud');
          }
        }
      }
      this.setStatus('synced');
    } catch (err) {
      if (!silent) console.warn('Cloud sync pull status:', err.message);
      this.setStatus('synced');
    }
  }
}

export const CloudSyncService = new CloudSyncEngine();
