declare namespace Model {
  interface BaseModel {
    id: string;
    created_at: string;
    updated_at: string;
  }

  interface User extends BaseModel {
    username: string;
    githubName?: string;
    wxUserId?: string;
  }

  interface Memo extends BaseModel {
    content: string;
    deleted_at?: string;
  }
}
