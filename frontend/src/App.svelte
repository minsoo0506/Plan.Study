<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Mylist from "./routes/Mylist.svelte"
  import Detail from "./routes/Detail.svelte"
  import TodoCreate from "./routes/TodoCreate.svelte"
  import Navigation from "./components/Navigation.svelte"
  import UserCreate from "./routes/UserCreate.svelte"
  import UserLogin from "./routes/UserLogin.svelte"
  import TodoModify from "./routes/TodoModify.svelte"
  import Mypage from "./routes/Mypage.svelte"
  import Search from "./routes/Search.svelte"
  import Otherpage from './routes/Otherpage.svelte'

  const routes = {
    '/': Home,
    '/mylist': Mylist,
    '/detail/:todo_id': Detail,
    '/todo-create': TodoCreate,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/todo-modify/:todo_id': TodoModify,
    '/mypage': Mypage,
    '/search': Search,
    '/otherpage/:username': Otherpage,
  }
</script>

<Navigation />
<Router {routes}/>


