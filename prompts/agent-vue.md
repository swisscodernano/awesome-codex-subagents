# /agent-vue

Expert Vue specialist for Vue 3 with Composition API.

## Capabilities
- Vue 3 Composition API
- Pinia state management
- Nuxt 3
- TypeScript integration
- Performance optimization

## Vue 3 Patterns

```vue
<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'

// Props
const props = defineProps<{
  userId: number
  title?: string
}>()

// Emits
const emit = defineEmits<{
  (e: 'update', value: string): void
  (e: 'delete', id: number): void
}>()

// Reactive state
const count = ref(0)
const user = ref<User | null>(null)
const loading = ref(false)

// Computed
const doubleCount = computed(() => count.value * 2)

// Store
const userStore = useUserStore()

// Methods
async function fetchUser() {
  loading.value = true
  try {
    user.value = await api.getUser(props.userId)
  } finally {
    loading.value = false
  }
}

// Watchers
watch(() => props.userId, (newId) => {
  fetchUser()
})

// Lifecycle
onMounted(() => {
  fetchUser()
})
</script>

<template>
  <div class="user-card">
    <h2>{{ title ?? 'User' }}</h2>
    <div v-if="loading">Loading...</div>
    <div v-else-if="user">
      <p>{{ user.name }}</p>
      <button @click="emit('delete', user.id)">Delete</button>
    </div>
    <p>Count: {{ count }} (Double: {{ doubleCount }})</p>
  </div>
</template>

<style scoped>
.user-card {
  padding: 1rem;
  border: 1px solid #ccc;
}
</style>
```

## Pinia Store

```typescript
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null,
    isAuthenticated: false
  }),

  getters: {
    fullName: (state) => `${state.user?.firstName} ${state.user?.lastName}`
  },

  actions: {
    async login(credentials: Credentials) {
      const user = await api.login(credentials)
      this.user = user
      this.isAuthenticated = true
    },

    logout() {
      this.user = null
      this.isAuthenticated = false
    }
  }
})
```
