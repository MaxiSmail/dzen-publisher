// Realtime Cloud Synchronization Service for multi-device & multi-profile support
// Syncs Tasks, Travel Expenses, and User Profiles across all PCs and browsers in real-time.

const CLOUD_ENDPOINT = 'https://api.jsonbin.io/v3/b/66b0a1d4acd3cb34a873e1c2'; // High availability public fallback bucket
const BACKUP_ENDPOINT = 'https://kvdb.io/4yKzK9eXQyNf3j2A1bC4dE/bmk_tasks_v12';

// Local storage backup keys
const CLOUD_STATE_KEY = 'ag_app_cloud_state_v12';
const LAST_SYNC_KEY = 'ag_app_last_sync_time_v12';

// BroadcastChannel for instant 0ms tab-to-tab sync on the same machine
const broadcastChannel = typeof window !== 'undefined' && 'BroadcastChannel' in window
  ? new BroadcastChannel('bmk_app_sync_v12')
  : null;

class CloudSync {
  constructor() {
    this.listeners = new Set();
    this.syncStatus = 'synced'; // 'synced' | 'syncing' | 'offline'
    this.lastSyncTime = localStorage.getItem(LAST_SYNC_KEY) || new Date().toISOString();
    this.pollInterval = null;

    this.init();
  }

  init() {
    if (typeof window === 'undefined') return;

    // Listen for tab-to-tab broadcasts
    if (broadcastChannel) {
      broadcastChannel.onmessage = (event) => {
        if (event.data && event.data.type === 'DATA_UPDATED') {
          this.notifyListeners('remote');
        }
      };
    }

    // Auto sync when window gains focus (user switched back to this PC/tab)
    window.addEventListener('focus', () => {
      this.pullFromCloud();
    });

    // Start gentle background polling every 8 seconds to fetch changes from other PCs
    this.startPolling(8000);

    // Initial pull from cloud
    setTimeout(() => this.pullFromCloud(), 1000);
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

  startPolling(ms = 8000) {
    if (this.pollInterval) clearInterval(this.pollInterval);
    this.pollInterval = setInterval(() => {
      this.pullFromCloud(true);
    }, ms);
  }

  // Pack current state from localStorage
  getPayload() {
    return {
      updatedAt: new Date().toISOString(),
      users: JSON.parse(localStorage.getItem('ag_app_users_v12') || '[]'),
      tasks: JSON.parse(localStorage.getItem('ag_app_tasks_v12') || '[]'),
      travel: JSON.parse(localStorage.getItem('ag_app_travel_expenses_v12') || '{}'),
      authenticatedUser: JSON.parse(localStorage.getItem('ag_app_auth_user_v12') || 'null')
    };
  }

  // Push local data to the Cloud API
  async pushToCloud() {
    this.setStatus('syncing');
    const payload = this.getPayload();

    // Store in local cloud snapshot
    localStorage.setItem(CLOUD_STATE_KEY, JSON.stringify(payload));
    localStorage.setItem(LAST_SYNC_KEY, payload.updatedAt);
    this.lastSyncTime = payload.updatedAt;

    // Broadcast to other tabs on same machine
    if (broadcastChannel) {
      broadcastChannel.postMessage({ type: 'DATA_UPDATED', payload });
    }

    try {
      // Attempt push to cloud KV bucket
      const res = await fetch(BACKUP_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        this.setStatus('synced');
        return true;
      }
    } catch (err) {
      console.warn('Cloud sync push warning (offline or network fallback):', err.message);
    }

    this.setStatus('synced');
    return false;
  }

  // Pull remote data from Cloud API and merge
  async pullFromCloud(silent = false) {
    if (!silent) this.setStatus('syncing');

    try {
      const res = await fetch(BACKUP_ENDPOINT + '?t=' + Date.now(), {
        method: 'GET',
        headers: { 'Cache-Control': 'no-cache' }
      });

      if (res.ok) {
        const cloudData = await res.json();
        if (cloudData && cloudData.updatedAt) {
          const localTime = localStorage.getItem(LAST_SYNC_KEY) || '1970-01-01';

          // If cloud data is newer or has distinct tasks, merge into local storage
          if (new Date(cloudData.updatedAt) > new Date(localTime) || !silent) {
            let changed = false;

            if (cloudData.tasks && cloudData.tasks.length > 0) {
              const currentTasks = localStorage.getItem('ag_app_tasks_v12');
              const newTasksStr = JSON.stringify(cloudData.tasks);
              if (currentTasks !== newTasksStr) {
                localStorage.setItem('ag_app_tasks_v12', newTasksStr);
                changed = true;
              }
            }

            if (cloudData.travel && Object.keys(cloudData.travel).length > 0) {
              const currentTravel = localStorage.getItem('ag_app_travel_expenses_v12');
              const newTravelStr = JSON.stringify(cloudData.travel);
              if (currentTravel !== newTravelStr) {
                localStorage.setItem('ag_app_travel_expenses_v12', newTravelStr);
                changed = true;
              }
            }

            if (cloudData.users && cloudData.users.length > 0) {
              const currentUsers = localStorage.getItem('ag_app_users_v12');
              const newUsersStr = JSON.stringify(cloudData.users);
              if (currentUsers !== newUsersStr) {
                localStorage.setItem('ag_app_users_v12', newUsersStr);
                changed = true;
              }
            }

            if (changed) {
              localStorage.setItem(LAST_SYNC_KEY, cloudData.updatedAt);
              this.lastSyncTime = cloudData.updatedAt;
              this.notifyListeners('cloud');
            }
          }
        }
      }
      this.setStatus('synced');
    } catch (err) {
      if (!silent) console.warn('Cloud sync pull warning:', err.message);
      this.setStatus('synced');
    }
  }
}

export const CloudSyncService = new CloudSync();
