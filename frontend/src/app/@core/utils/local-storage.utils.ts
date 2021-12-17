export enum StorageItem {
  Auth = 'App/auth',
  Theme = 'App/theme',
  User = 'App/user',
  Email = 'App/email',
  Cart = 'App/cart',
  Products = 'App/products',
  PageMessages = 'App/page-messages',
}

export const getStorageItem = (itemName: StorageItem): unknown | null => {
  const item = localStorage.getItem(itemName);
  return item ? JSON.parse(item) : null;
};

export const getRawStorageItem = (itemName: StorageItem): unknown | null => {
  const item = localStorage.getItem(itemName);
  return item;
};

export const setStorageItem = (itemName: StorageItem, value: unknown): void => {
  localStorage.setItem(itemName, JSON.stringify(value));
};

export const removeStorageItem = (itemName: StorageItem): unknown | null => {
  let value = getStorageItem(itemName);
  localStorage.removeItem(itemName);
  return value;
};

export const addToStorageList = (itemName: StorageItem, value: unknown): unknown => {
  let list = getStorageItem(itemName);
  if(list && Array.isArray(list))
    list.push(value);
  else
    list = [value]
  localStorage.setItem(itemName, JSON.stringify(value));
  return list;
};


