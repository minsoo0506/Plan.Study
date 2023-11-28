<script>
    import { link, push } from 'svelte-spa-router'
</script>
  
<div class="d-flex flex-column align-items-center justify-content-center vh-100">
    <div class="text-center w-100">
        <h1>Plan.Study</h1>
    </div>
    <div class="card p-3 text-center w-50 d-flex flex-column align-items-center">
        <button class="btn btn-primary mb-2 w-100" style="height: 3rem;" on:click={() => push('/user-login')}>로그인</button>
        <button class="btn btn-secondary w-100" style="height: 3rem;" on:click={() => push('/user-create')}>회원가입</button>
    </div>
</div>
