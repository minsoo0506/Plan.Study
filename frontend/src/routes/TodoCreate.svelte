<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"

    let error = {detail:[]}
    let subject = ''
    let content = ''
    let category = ''

    function post_todo(event) {
        event.preventDefault()
        let url = "/api/todo/create"
        let params = {
            subject: subject,
            content: content,
            category: category,
        }
        fastapi('post', url, params, 
            (json) => {
                push("/mylist")
            },
            (json_error) => {
                error = json_error
            }
        )
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">공부 계획 등록</h5>
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="subject">제목</label>
            <input type="text" class="form-control" bind:value="{subject}">
        </div>
        <div class="mb-3">
            <label for="category">카테고리</label>
            <select class="form-control" bind:value="{category}">
                <option value="" disabled selected>공부 분야 선택</option>
                <option>철학</option>
                <option>종교</option>
                <option>사회학</option>
                <option>언어</option>
                <option>자연과학</option>
                <option>기술과학</option>
                <option>예술</option>
                <option>문학</option>
                <option>역사</option>
                <option>기타</option>
            </select>
        </div>
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value="{content}"></textarea>
        </div>
        <button class="btn btn-primary" on:click={post_todo}>등록하기</button>
    </form>
</div>