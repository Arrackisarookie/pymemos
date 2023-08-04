import api from "../helpers/api";
import appStore from "../stores/appStore";

class UserService {
  public getState() {
    return appStore.getState().userState;
  }

  public async doLogin() {
    const { data: user } = await api.getUserInfo();
    if (user) {
      appStore.dispatch({
        type: "LOG_IN",
        payload: { user },
      });
    } else {
      await userService.doLogOut();
    }
    return user;
  }

  public async doLogOut() {
    appStore.dispatch({
      type: "LOG_OUT",
      payload: null,
    });
    api.logout().catch(() => {
      // do nth
    });
  }

  public async checkUsernameUsable(username: string): Promise<boolean> {
    const { data: isUsable } = await api.checkUsernameUsable(username);
    return isUsable;
  }

  public async updateUsername(username: string): Promise<void> {
    await api.updateUserinfo(username);
  }

  public async removeGithubName(): Promise<void> {
    await api.updateUserinfo(undefined, undefined, "");
  }

  public async checkPasswordValid(password: string): Promise<boolean> {
    const { data: isValid } = await api.checkPasswordValid(password);
    return isValid;
  }

  public async updatePassword(password: string): Promise<void> {
    await api.updateUserinfo(undefined, password);
  }

  public async updateWxUserId(wxUserId: string): Promise<void> {
    await api.updateUserinfo(undefined, undefined, undefined, wxUserId);
  }
}

const userService = new UserService();

export default userService;
