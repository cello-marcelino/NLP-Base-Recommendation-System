import { ref } from 'vue';

export const toastState = ref({
  show: false,
  message: '',
  type: 'error' // 'error' atau 'success'
});

export const showToast = (message, type = 'error') => {
  toastState.value = { show: true, message, type };
  // Toast akan hilang otomatis setelah 3.5 detik
  setTimeout(() => {
    toastState.value.show = false;
  }, 3500);
};