export const streamProgress = (judul, abstrak, kRank, alpha, beta, onMessage, onError, onComplete) => {
  const url = `http://127.0.0.1:5050/api/rekomendasi/stream?judul=${encodeURIComponent(judul)}&abstrak=${encodeURIComponent(abstrak)}&k=${kRank}&bobot_lexical=${alpha}&bobot_semantic=${beta}`;
  const eventSource = new EventSource(url);
  
  eventSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (data.is_complete) {
        eventSource.close();
        if (data.step === -1) {
          if (onError) onError(new Error(data.message));
        } else {
          if (onComplete) onComplete(data.payload);
        }
      } else {
        if (onMessage) onMessage(data);
      }
    } catch (e) {
      if (onError) onError(e);
    }
  };

  eventSource.onerror = (error) => {
    eventSource.close();
    if (onError) onError(error);
  };

  return eventSource;
};
