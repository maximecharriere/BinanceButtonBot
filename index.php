<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
  <script src="https://cdn.jsdelivr.net/npm/hammerjs/hammer.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js/dist/chart.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation/dist/chartjs-plugin-annotation.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom/dist/chartjs-plugin-zoom.min.js"></script>


  <style type="text/css">
    .myChart {
      width: 98vw;
      height: 98vh;
    }
  </style>
</head>

<body>

  <?php
  $login = json_decode(file_get_contents("db_login.json"), true);
  $hostname   = "localhost";
  $username   = $login["user"];
  $password   = $login["password"];
  $dbname     = $login["database"];

  // Create connection
  $connection = new mysqli($hostname, $username, $password, $dbname);

  // Check connection
  if ($connection->connect_error) {
    die("Connection failed: " . $connection->connect_error);
  }

  // Get data
  $sql_query = "SELECT * FROM binance_btn_stats ORDER BY timestamp_unix ASC";
  // $sql_query = "SELECT timestamp_unix*1000 AS timestamp_unix_ms, participants_tot, countdown_min FROM binance_btn_stats ORDER BY timestamp_unix ASC";
  $result = $connection->query($sql_query);
  $connection->close();

  $data = $result->fetch_all(MYSQLI_ASSOC);

  ?>

  <div class="myChart">
    <canvas id="myChart"></canvas>
  </div>

  <script>
    Date.prototype.addDays = function(days) {
      var date = new Date(this.valueOf());
      date.setDate(date.getDate() + days);
      return date;
    }

    // Setup Block
    const start_date = new Date("Mars 15, 2022 00:00:00");
    const end_date = start_date.addDays(90);
    const timestamp = <?php echo json_encode(array_column($data, 'timestamp_unix')) ?>;
    const participants_tot = <?php echo json_encode(array_column($data, 'participants_tot')) ?>;
    const countdown_min = <?php echo json_encode(array_column($data, 'countdown_min')) ?>;
    const num_data = timestamp.length;

    var datetime = [];
    var participants = new Array(num_data);
    timestamp.forEach((o) => datetime.push(new Date(o * 1000)));
    for (let i = 1; i < num_data; i++) {
      participants[i] = (participants_tot[i] - participants_tot[i - 1]) / ((timestamp[i] - timestamp[i - 1]) / 60);
    }
    participants[0] = participants[1];

    const data = {
      labels: datetime,
      datasets: [{
          type: 'scatter',
          label: 'New participants / minute',
          yAxisID: 'y',
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: 'rgb(255, 99, 132)',
          data: participants,
        },
        {
          type: 'scatter',
          label: 'Minimum countdown in a minute',
          yAxisID: 'y1',
          borderColor: 'rgb(100, 99, 255)',
          backgroundColor: 'rgb(100, 99, 255)',
          data: countdown_min,
        },
      ]
    };

    // Config Block

    const config = {
      type: 'scatter',
      data: data,
      options: {
        animation: false,
        responsive: true,
        maintainAspectRatio : false,
        interaction: {
          mode: 'nearest',
        },
        stacked: false,
        plugins: {
          title: {
            display: true,
            text: 'Binance Play Button Statistics'
          },
          zoom: {
            pan: {
              enabled: true,
              mode: 'x',
            },
            limits: {
              x: {
                min: start_date.addDays(-1),
                max: end_date.addDays(1),
                minRange: new Date(1000*60*60*24)
              },
            },
            zoom: {
              wheel: {
                enabled: true,
              },
              pinch: {
                enabled: true
              },
              mode: 'x',
            }
          },
          annotation: {
            annotations: {
              lineStart: {
                type: 'line',
                borderColor: 'red',
                borderWidth: 3,
                scaleID: 'x',
                value: start_date,
                label: {
                  backgroundColor: 'red',
                  content: 'Start of game',
                  enabled: true,
                },
              },
              lineEnd: {
                type: 'line',
                borderColor: 'red',
                borderWidth: 3,
                scaleID: 'x',
                value: end_date,
                label: {
                  backgroundColor: 'red',
                  content: 'End of game',
                  enabled: true,
                },
              },
            },
          },
        },
        scales: {
          x: {
            type: 'time',
            title: {
              display: true,
              text: 'Date'
            },
            ticks: {
              autoSkip: true,
              maxRotation: 0,
              major: {
                enabled: true
              },
              font: function(context) {
                if (context.tick && context.tick.major) {
                  return {
                    weight: 'bold',
                  };
                }
              },
              color: function(context) {
                return (context.tick && context.tick.major) ? '#000000' : '#545454';
              },
            },
          },
          y: {
            type: 'linear',
            display: true,
            position: 'left',
            title: {
              display: true,
              text: 'Clic / Minute',
            },
            min: 0,
            max: 25,
          },
          y1: {
            type: 'linear',
            display: true,
            position: 'right',
            title: {
              display: true,
              text: 'Second'
            },
            min: 0,
            max: 60,
            grid: {
              drawOnChartArea: false, // only want the grid lines for one axis to show up
            },
          },
        },
      },
    };

    // Render Block

    const myChart = new Chart(
      document.getElementById('myChart'),
      config
    );
  </script>
</body>

</html>