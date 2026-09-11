import { useState } from 'react';
export function useApi() {
  const [loading, setLoading] = useState(false);
  return { loading };
}
