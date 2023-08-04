type ResponseType<T = unknown> = {
  succeed: boolean;
  status: number;
  message: string;
  data: T;
};

async function get<T>(url: string): Promise<ResponseType<T>> {
  const response = await fetch(url, {
    method: "GET",
  });
  const resData = (await response.json()) as ResponseType<T>;

  if (!resData.succeed) {
    throw resData;
  }

  return resData;
}

async function post<T>(url: string, data?: BasicType): Promise<ResponseType<T>> {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const resData = (await response.json()) as ResponseType<T>;

  if (!resData.succeed) {
    throw resData;
  }

  return resData;
}

async function patch<T>(url: string, data?: BasicType): Promise<ResponseType<T>> {
  const response = await fetch(url, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const resData = (await response.json()) as ResponseType<T>;

  if (!resData.succeed) {
    throw resData;
  }

  return resData;
}


async function delete_<T>(url: string, data?: BasicType): Promise<ResponseType<T>> {
  const response = await fetch(url, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const resData = (await response.json()) as ResponseType<T>;

  if (!resData.succeed) {
    throw resData;
  }

  return resData;
}

namespace api {
  export function getUserInfo() {
    return get<Model.User>("/api/me");
  }

  export function login(username: string, password: string) {
    return post("/api/login", { username, password });
  }

  export function signup(username: string, password: string) {
    return post("/api/signup", { username, password });
  }

  export function logout() {
    return post("/api/logout");
  }

  export function checkUsernameUsable(username: string) {
    return get<boolean>("/api/user/checkusername?username=" + username);
  }

  export function checkPasswordValid(password: string) {
    return post<boolean>("/api/user/checkpassword", { password });
  }

  export function updateUserinfo(username?: string, password?: string, githubName?: string, wxUserId?: string) {
    return post("/api/user/update", {
      username,
      password,
      githubName,
      wxUserId,
    });
  }

  export function getMyMemos() {
    return get<Model.Memo[]>("/api/memo");
  }

  export function getMyDeletedMemos() {
    return get<Model.Memo[]>("/api/trash/memo");
  }

  export function createMemo(content: string) {
    return post<Model.Memo>("/api/memo", { content });
  }

  export function getMemoById(id: string) {
    return get<Model.Memo>("/api/memo/" + id);
  }

  export function hideMemo(memoId: string) {
    return delete_("/api/memo/" + memoId);
  }

  export function restoreMemo(memoId: string) {
    return post("/api/memo/restore", {
      memoId,
    });
  }

  export function deleteMemo(memoId: string) {
    return post("/api/memo/delete", {
      memoId,
    });
  }

  export function updateMemo(memoId: string, content: string) {
    return patch<Model.Memo>("/api/memo/" + memoId, { content });
  }

  export function getLinkedMemos(memoId: string) {
    return get<Model.Memo[]>("/api/memo/"+memoId);
  }

  export function removeGithubName() {
    return post("/api/user/updategh", { githubName: "" });
  }
}

export default api;
