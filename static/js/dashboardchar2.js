const ctx2 = document.getElementById('doughnutchart');

new Chart(ctx2, {
  type: 'doughnut',
  data: {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
      label: '# of Votes',
      data: [12, 19, 3, 5, 2, 3],
      borderWidth: 1,
      backgroundColor:[
        'rgba(134, 198, 201, 0.8)',
        'rgba(255, 183, 108, 0.7)',
        'rgba(209, 156, 226, 0.9)',
        'rgba(82, 184, 85, 0.6)',
        'rgba(247, 125, 164, 0.8)',
        'rgba(112, 218, 244, 0.7)'
      
    ]}]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});