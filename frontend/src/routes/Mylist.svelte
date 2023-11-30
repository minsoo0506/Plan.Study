<script>
    import fastapi from "../lib/api"
    import { link, push } from 'svelte-spa-router'
    import { page, keyword, is_login } from "../lib/store"
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')

    let todo_list = []
    let completed = []
    let size = 10
    let total = 0
    let kw = ''
    $: total_page = Math.ceil(total/size)

    function get_todo_list() {
        let params = {
            page: $page,
            size: size,
            keyword: $keyword,
        }
        fastapi('get', '/api/todo/list', params, (json) => {
            todo_list = json.todo_list
            completed = todo_list.map(todo => todo.completed == 1)
            total = json.total
            kw = $keyword
        })
    }

    function updateCompleted(todo, event) {
        let params = {
            todo_id: todo.id,
            completed: event.target.checked,
        }
        fastapi('put', '/api/todo/update_completed', params, (json) => {
            get_todo_list()
        })
    }

    $:$page, $keyword, get_todo_list()
</script>

<div class="container my-3">
    <div class="row my-3">
        <div class="col-6">
            <a use:link href="/todo-create"
                class="btn btn-primary {$is_login ? '' : 'disabled'}">Let's Plan!
            </a>
        </div>
        <div class="col-6">
            <div class="input-group">
                <input type="text" class="form-control" bind:value="{kw}">
                <button class="btn btn-outline-secondary" on:click={() => {$keyword = kw, $page = 0}}>
                    찾기
                </button>
            </div>
        </div>
    </div>
    <table class="table">
        <thead>
        <tr class="text-center table-info">
            <th>no.</th>
            <th style="width:50%">제목</th>
            <th>달성 <i class="bi bi-bookmark-check"></i></th> <!-- 수정된 부분 -->
            <th>작성일시</th>
        </tr>
        </thead>
        <tbody>
        {#each todo_list as todo, i}
        <tr class="text-center">
            <td>{ total - ($page * size) - i }</td>
            <td class="text-center">
                <a use:link href="/detail/{todo.id}">{todo.subject}</a>
                {#if todo.comments && todo.comments.length > 0 }
                <span class="text-danger small mx-2">{todo.comments.length}</span>
                {/if}
            </td>
            <!--<td>{ todo.user ? todo.user.username : "" }</td>-->
            <td>
                <input type="checkbox" id="completed-{i}" bind:checked={todo.completed} on:change="{(event) => updateCompleted(todo, event)}">
                <label for="completed-{i}">{todo.completed ? '완료' : '진행중'}</label>
            </td>
            <td>{moment(todo.create_date).format("YYYY년 MM월 DD일")}</td>
        </tr>
        {/each}
        </tbody>
    </table>
    <!-- 페이징처리 시작 -->
    <ul class="pagination justify-content-center">
        <!-- 이전페이지 -->
        <li class="page-item {$page <= 0 && 'disabled'}">
            <button class="page-link" on:click="{() => $page--}">이전</button>
        </li>
        <!-- 페이지번호 -->
        {#each Array(total_page) as _, loop_page}
        {#if loop_page >= $page-5 && loop_page <= $page+5} 
        <li class="page-item {loop_page === $page && 'active'}">
            <button on:click="{() => $page = loop_page}" class="page-link">{loop_page+1}</button>
        </li>
        {/if}
        {/each}
        <!-- 다음페이지 -->
        <li class="page-item {$page >= total_page-1 && 'disabled'}">
            <button class="page-link" on:click="{() => $page++}">다음</button>
        </li>
    </ul>
    <!-- 페이징처리 끝 -->
</div>