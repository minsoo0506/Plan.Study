<script>
    import { onMount, afterUpdate } from 'svelte'
    import { Chart, DoughnutController, BarController, CategoryScale, LinearScale, ArcElement, BarElement, Title, Tooltip, Legend } from 'chart.js'
    import { is_login, username } from "../lib/store"
    import fastapi from "../lib/api"
    import { get } from 'svelte/store'

    Chart.register(DoughnutController, BarController, CategoryScale, LinearScale, ArcElement, BarElement, Title, Tooltip, Legend)

    let userData = {}
    let completionChart = null
    let categoryChart = null
    let userRank = 0

    async function get_user_data() {
        if ($is_login) {
            fastapi('get', `/api/todo/user-data/${$username}`, {}, (json) => {
                userData = json
                userRank = userData.userRank
            })
        }
    }

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
                    backgroundColor: ['skyblue', 'lightgray']
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

        const categoryCtx = document.getElementById('categoryChart').getContext('2d')
        categoryChart = new Chart(categoryCtx, {
            type: 'bar',
            data: {
                datasets: [{
                    data: Object.values(userData.categoryCounts),
                    backgroundColor: 'lightgreen'
                }],
                labels: Object.keys(userData.categoryCounts)
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        },
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        })
    }

    onMount(async () => {
        get_user_data()
    })

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
                    <h5 class="card-title">User ID: {$username}</h5>
                    <hr class="my-4 bg-light">
                    <h5 class="card-title">User Rank: {userData.userRank !== undefined ? userData.userRank : 'Loading...'}</h5>
                    <p class="text-muted">랭크 선정 방식 : 업로드 된 공부 리스트의 총 개수를 유저들끼리 비교</p>
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

