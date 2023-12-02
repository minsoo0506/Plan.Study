<script>
    import { onMount, afterUpdate } from 'svelte'
    import { Chart, DoughnutController, BarController, CategoryScale, LinearScale, ArcElement, BarElement, Title, Tooltip, Legend } from 'chart.js'
    import { is_login, username } from "../lib/store"
    import fastapi from "../lib/api"
    import { get } from 'svelte/store'
    import { push, location } from 'svelte-spa-router'
    export let params

    Chart.register(DoughnutController, BarController, CategoryScale, LinearScale, ArcElement, BarElement, Title, Tooltip, Legend)

    let otherUsername
    let userData = {}
    let completionChart = null
    let categoryChart = null
    let categoryCounts = {}
    let categories = ['철학', '종교', '사회학', '언어', '자연과학', '기술과학', '예술', '문학', '역사', '기타']
    let userRank = 0

    onMount(() => {
        if (params.username) {
            otherUsername = params.username;
            get_user_data();
        }
    })

    async function get_user_data() {
        console.log(otherUsername)
        await fastapi('get', `/api/todo/user-data/${otherUsername}`, {}, (json) => {
            userData = json
            userRank = userData.userRank
            categoryCounts = userData.categoryCounts  // 백엔드에서 제공하는 카테고리별 할 일 개수 데이터를 가져온다.
        })
    }

    const categoryColors = [
        'rgba(255, 99, 132, 0.2)',  // 빨강
        'rgba(255, 159, 64, 0.2)',  // 주황
        'rgba(255, 205, 86, 0.2)',  // 노랑
        'rgba(75, 192, 192, 0.2)',  // 초록
        'rgba(54, 162, 235, 0.2)',  // 파랑
        'rgba(153, 102, 255, 0.2)',  // 남색
        'rgba(201, 203, 207, 0.2)',   // 보라
        'rgba(255, 99, 71, 0.2)',    // 토마토
        'rgba(127, 255, 212, 0.2)',   // 아쿠아마린
        'rgba(218, 165, 32, 0.2)'    // 골드
    ];

    function updateCharts() {
        if (completionChart) {
            completionChart.destroy()
        }
        if (categoryChart) {
            categoryChart.destroy()
        }
        
        const completionCtx = document.getElementById('completionChart').getContext('2d')
        completionChart = new Chart(completionCtx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [userData.completionRate, 100 - userData.completionRate],
                    backgroundColor: ['rgba(0, 123, 255, 0.5)', 'rgba(128, 128, 128, 0.1)'],
                }],
                labels: ['Completed', 'Not completed']
            },
            options: {
                cutout: '80%',
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: false
                    }
                }
            }
        })

        const categoryCtx = document.getElementById('categoryChart').getContext('2d');
            categoryChart = new Chart(categoryCtx, {
                type: 'bar',
                data: {
                    labels: Object.keys(categoryCounts),  // 카테고리 이름을 레이블로 사용한다.
                    datasets: [{
                        label: '해당 카테고리의 개수', 
                        data: Object.values(categoryCounts),  // 카테고리별 할 일 개수를 데이터로 사용한다.
                        backgroundColor: categoryColors, // 미리 지정한 색상을 사용 
                        borderColor: categoryColors, // 미리 지정한 색상을 사용
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1 // y축의 단위를 1로 설정
                            }
                        }
                    }
                }
            })
    }

    afterUpdate(() => {
        if ('completionRate' in userData && 'categoryCounts' in userData) {
            updateCharts()
        }
    })
</script>

<div class="container mt-5">
    <div class="row">
        <div class="col-lg-6 d-flex">
            <div class="card flex-fill">
                <div class="card-header bg-primary text-white">User Info</div>
                <div class="card-body">
                    <h5 class="card-title">User ID: {otherUsername}</h5>
                    <hr class="my-4 bg-light">
                    <h5 class="card-title">User Rank: {userData.userRank !== undefined ? userData.userRank : 'Loading...'}</h5>
                    <p class="text-muted">업로드 된 공부 리스트의 총 개수를 유저들끼리 비교</p>
                </div>
            </div>
        </div>
        <div class="col-lg-6 d-flex">
            <div class="card flex-fill" id="completion">
                <div class="card-header bg-primary text-white">Completion Rate</div>
                <div class="card-body d-flex align-items-center justify-content-center">
                    <div class="chart-container position-relative">
                        <canvas id="completionChart"></canvas>
                        <div class="chart-text position-absolute top-50 start-50 translate-middle fs-4">
                            {userData ? `${userData.completionRate}%` : 'Loading...'}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="row mt-5">
        <div class="col-lg-12">
            <div class="card" id="category">
                <div class="card-header bg-primary text-white">Category Chart</div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="categoryChart"></canvas>
                    </div>
                    <p class="text-center">Total list: {userData.totalListCount !== undefined ? userData.totalListCount : 'Loading...'}</p>
                </div>
            </div>
        </div>
    </div>
</div>