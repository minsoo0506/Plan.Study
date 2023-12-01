<script>
    import { onMount, afterUpdate } from 'svelte'
    import { Chart, DoughnutController, BarController, CategoryScale, LinearScale, ArcElement, BarElement, Title, Tooltip, Legend } from 'chart.js'
    import { is_login, username } from "../lib/store"
    import fastapi from "../lib/api"

    Chart.register(DoughnutController, BarController, CategoryScale, LinearScale, ArcElement, BarElement, Title, Tooltip, Legend)

    let userData = {}
    let completionChart = null
    let categoryChart = null

    async function get_user_data() {
        if ($is_login) {
            fastapi('get', `/api/todo/user-data/${$username}`, {}, (json) => {
                userData = json
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

    onMount(() => {
        get_user_data()
    })

    afterUpdate(() => {
        if ('completionRate' in userData && 'categoryCounts' in userData) {
            updateCharts()
        }
    })
</script>

<style>
    #completion, #category {
        height: 400px; /* Adjust this value as needed */
        overflow: auto; /* Add a scrollbar if the content overflows */
    }
</style>

<div class="container mt-4">
    <div class="card">
        <div class="card-header bg-primary text-white">{userData.username}</div>
        <div class="card-body">
            <h5 class="card-title">Total lists: {userData ? userData.totalListCount : 'Loading...'}</h5>
        </div>
    </div>
    <div class="row mt-4">
        <div class="col-lg-6">
            <div class="card" id="completion">
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
        <div class="col-lg-6">
            <div class="card" id="category">
                <div class="card-header bg-primary text-white">Category Chart</div>
                <div class="card-body">
                    <div class="chart-container">
                        <canvas id="categoryChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>