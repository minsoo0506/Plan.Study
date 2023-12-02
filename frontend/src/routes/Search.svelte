<script>
    import { push } from 'svelte-spa-router';
    import fastapi from '../lib/api';
    import { writable } from 'svelte/store';

    let searchQuery = writable('');
    let searchResults = [];
    let noResults = false; // 검색 결과가 없음을 나타내는 플래그
    let error = null;

    async function searchUser() {
        try {
            fastapi('get', `/api/todo/user-data/${$searchQuery}`, {}, (data) => {
                console.log(data);
                if (!data) {
                    noResults = true
                } else {
                    // If there's at least one search result, navigate to the first user's page
                    push(`/otherpage/${data.username}`)
                }
            })
        } catch (err) {
            console.error(err)
            error = err
        }
    }
</script>

<div style="display: flex; justify-content: center; align-items: center; height: 100vh; background: rgba(135,206,235,0.5);">
    <div style="background: rgba(135,206,235,0); padding: 20px; border-radius: 10px; width: 600px;">
        <p style="color: black; text-align: center; font-weight: bold; font-size: 2em;">상대방의 아이디를 검색하세요</p>
        <div class="input-group mb-3">
            <input type="text" class="form-control" bind:value={$searchQuery} placeholder="Search for a user" style="border-top-left-radius: 30px; border-bottom-left-radius: 30px; font-size: 1.5em; height: 60px; border-right: none;">
            <div class="input-group-append">
                <button class="btn btn-primary" type="button" on:click={searchUser} style="border-top-right-radius: 30px; border-bottom-right-radius: 30px; font-size: 1.5em; height: 60px;">Search</button>
            </div>
        </div>
        <!-- API 호출에서 오류가 발생했을 때 오류 메시지를 표시 -->
        {#if error}
            <p style="color: red;">{error.message}</p>
        {/if}
        <!-- 검색 결과가 없을 때 메시지를 표시 -->
        {#if noResults}
            <p style="color: red;">검색 결과가 없습니다.</p>
        {/if}
    </div>
</div>