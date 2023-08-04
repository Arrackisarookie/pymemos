export interface State {
  user: Model.User | null;
}

interface LogInAction {
  type: "LOG_IN";
  payload: State;
}

interface LogOutAction {
  type: "LOG_OUT";
  payload: null;
}

export type Actions = LogInAction | LogOutAction;

export function reducer(state: State, action: Actions): State {
  switch (action.type) {
    case "LOG_IN": {
      return {
        user: action.payload.user,
      };
    }
    case "LOG_OUT": {
      return {
        user: null,
      };
    }
    default: {
      return state;
    }
  }
}

export const defaultState: State = { user: null };
