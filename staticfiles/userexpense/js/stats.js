const renderChat = (data, labels) => {
    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: 'Last 6 months eppenses',
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {           
            title: {
                display: true,
                text: 'Expenses per category'
            }
        }
    });

};

const getChartData=()=>{
    fetch('/expenses/expenses_summery').then(res=>res.json()).then(result=>{
        console.log('result',result)
        const category_data = result.expense_category_amount;
        const [labels,data] = [
            Object.keys(category_data),
            Object.values(category_data),
        ];
        renderChat(data,labels);
    });
};



document.onload=getChartData();