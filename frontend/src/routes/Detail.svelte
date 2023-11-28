<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { link, push } from 'svelte-spa-router'
    import { is_login, username } from "../lib/store"
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')

    export let params = {}
    let todo_id = params.todo_id
    let todo = {content: ''}
    let content = ""
    let error = {detail:[]}

    function get_todo() {
        fastapi("get", "/api/todo/detail/" + todo_id, {}, (json) => {
            todo = json
        })
    }

    get_todo()

    function delete_todo(_todo_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/todo/delete"
            let params = {
                todo_id: _todo_id
            }
            fastapi('delete', url, params, 
                (json) => {
                    push('/mylist')
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }
</script>

<div class="container my-3">
    <!-- 질문 -->
    <h2 class="border-bottom py-2">{todo.subject}</h2>
    <div class="card my-3">
        <div class="card-body">
            <p>{todo.content}</p>
            <div class="d-flex justify-content-end">
                {#if todo.modify_date }
                <div class="badge bg-light text-dark p-2 text-start mx-3">
                    <div class="mb-2">modified at</div>
                    <div>{moment(todo.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{ todo.user ? todo.user.username : ""}</div>
                    <div>{moment(todo.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
            </div>
            <div class="my-3">
                {#if todo.user && $username === todo.user.username }
                <a use:link href="/todo-modify/{todo.id}" 
                    class="btn btn-sm btn-outline-secondary">수정</a>
                <button class="btn btn-sm btn-outline-secondary"
                    on:click={() => delete_todo(todo.id)}>삭제</button>
                {/if}
            </div>
        </div>
    </div>

    <button class="btn btn-secondary" on:click="{() => {
        push('/mylist')
    }}">목록으로</button>
</div>
   