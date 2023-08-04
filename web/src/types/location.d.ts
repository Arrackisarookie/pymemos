interface Duration {
  from: number;
  to: number;
}

interface Query {
  tag: string;
  duration: Duration | null;
  type: MemoSpecType | "";
  text: string;
  filter: string;
}

type AppRouter = "/" | "/login" | "/recycle" | "/setting";

interface AppLocation {
  pathname: AppRouter;
  hash: string;
  query: Query;
}
