import { ref } from 'vue';

export const toastState = ref({
  show: false,
  message: '',
  type: 'error'
});

export const showToast = (message, type = 'error') => {
  toastState.value = { show: true, message, type };
  setTimeout(() => {
    toastState.value.show = false;
  }, 3000);
};
