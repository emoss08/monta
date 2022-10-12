const ACCESS_TOKEN = "access_token" as string;

/**
 * @description get token form localStorage
 */
export const getToken = (): string | null => {
  return window.localStorage.getItem(ACCESS_TOKEN);
};

/**
 * @description save token into localStorage
 * @param access_token: string
 */
export const saveToken = (access_token: string): void => {
  return window.localStorage.setItem(ACCESS_TOKEN, access_token);
};

/**
 * @description remove token form localStorage
 */
export const destroyToken = (): void => {
  return window.localStorage.removeItem(ACCESS_TOKEN);
};

export default { getToken, saveToken, destroyToken };
