<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>基地调研</title>
    <!-- CSS Files -->
    <link rel="stylesheet" href="dist/css/bootstrap.min.css" integrity="sha384-/Y6pD6FV/Vv2HJnA6t+vslU6fwYXjCFtcEpHbNJ0lyAFsXTsjBbfaDjzALeQsN6M" crossorigin="anonymous">
</head>
<body>
    <?php
    $filename = 'data/bike.json';
    $handle = fopen($filename, "r");
    $contents = fread($handle, filesize($filename));
    fclose($handle);
    $data = json_decode($contents);
    $timeline = array();
    foreach ($data as $key => $value) {
        $time = $value[0];
        $lo = $value[1];
        $la = $value[2];
        $num = $value[5];
        if (in_array($time, $timeline) == FALSE) {
            array_push($timeline, $time);
        }
        $pos = array_search($time, $timeline);
        if ($pos == 0) {
            $diff = 0;
        } else {
            $past = $timeline[$pos-1];
            foreach ($data as $p_value) {
                if ($p_value[0] == $past and $p_value[1] == $lo and $p_value[2] == $la) {
                    $diff = $num - $p_value[3];
                    break;
                }
            }
        }
        $data[$key] = array($time, $lo, $la, $num, $diff);
    }
    ?>
    <div id="dropdownMenu" class="dropdown">
      <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
        选择时间
      </button>
      <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
        <?php
        foreach ($timeline as $time) {
            echo "<a class='dropdown-item' href='#'>{$time}</a>";
        }
        ?>
      </div>
    </div>
    <div id="map-wrap" style="height:600px;width:1000px;" ></div>
    <!-- Javascript Files -->
    <!--引入百度地图的jssdk，这里需要使用你在百度地图开发者平台申请的 ak-->
    <script src="http://api.map.baidu.com/api?v=2.0&ak=61553fa09c9b4ddbf466b517a239b5c7"></script>
    <!-- 引入 ECharts -->
    <script src="dist/js/echarts.min.js"></script>
    <!-- 引入百度地图扩展 -->
    <script src="dist/js/extension/bmap.min.js"></script>
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="dist/js/jquery-3.2.1.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="dist/js/popper.min.js" integrity="sha384-b/U6ypiBEHpOf/4+1nzFpr53nxSS+GLCkfwBdFNTxtclqqenISfwAzpKaMNFNmj4" crossorigin="anonymous"></script>
    <script src="dist/js/bootstrap.min.js" integrity="sha384-h0AbiXch4ZDo7tp9hKZ4TsHbi047NrKGLO3SEJAg45jXxnGIfYzk4Si90RDIqNm1" crossorigin="anonymous"></script>
    <script type="text/javascript">
        $('#dropdownMenu a').on('click', function(){
            var time = $(this).text();
            $('#map-wrap').data('time', time);
            $('#dropdownMenuButton').html(time);
            changeSnapshot();
        });
    </script>
    <script type="text/javascript">
        $(document).ready( function () {
            var time = $('#dropdownMenu a:last-child').text();
            window.init_time = time;
            $('#map-wrap').data('time', time);

            var data = JSON.parse( <?php echo "'".json_encode($data)."'" ?> );
            snapshots = {}
            for (i=0; i<data.length; i++) {
                var row = data[i];
                var time = row[0];
                if (snapshots[time]) {
                    snapshots[time].push(data[i].slice(1,data.length));
                } else {
                    snapshots[time] = []
                }
            }
            chart = echarts.init(document.getElementById('map-wrap'));
            console.log(window.init_time);
            var option = {
                backgroundColor: '#404a59',
                title: {
                    text: '基地附近共享单车分布图',
                    subtext: 'Developed by hackrflov',
                    left: 'center',
                    textStyle: {
                        color: '#fff'
                    }
                },
                tooltip: {
                    trigger: 'item'
                },
                bmap: {
                    center: [121.500901000, 31.257057500],
                    zoom: 15,
                    roam: true,
                    mapStyle: {
                        styleJson: [
                            {
                                'featureType': 'water',
                                'elementType': 'all',
                                'stylers': {
                                    'color': '#044161'
                                }
                            },
                            {
                                'featureType': 'land',
                                'elementType': 'all',
                                'stylers': {
                                    'color': '#004981'
                                }
                            },
                            {
                                'featureType': 'boundary',
                                'elementType': 'geometry',
                                'stylers': {
                                    'color': '#064f85'
                                }
                            },
                            {
                                'featureType': 'railway',
                                'elementType': 'all',
                                'stylers': {
                                    'visibility': 'off'
                                }
                            },
                            {
                                'featureType': 'highway',
                                'elementType': 'geometry',
                                'stylers': {
                                    'color': '#004981'
                                }
                            },
                            {
                                'featureType': 'highway',
                                'elementType': 'geometry.fill',
                                'stylers': {
                                    'color': '#005b96',
                                    'lightness': 1
                                }
                            },
                            {
                                'featureType': 'highway',
                                'elementType': 'labels',
                                'stylers': {
                                    'visibility': 'off'
                                }
                            },
                            {
                                'featureType': 'arterial',
                                'elementType': 'geometry',
                                'stylers': {
                                    'color': '#004981'
                                }
                            },
                            {
                                'featureType': 'arterial',
                                'elementType': 'geometry.fill',
                                'stylers': {
                                    'color': '#00508b'
                                }
                            },
                            {
                                'featureType': 'poi',
                                'elementType': 'all',
                                'stylers': {
                                    'visibility': 'off'
                                }
                            },
                            {
                                'featureType': 'green',
                                'elementType': 'all',
                                'stylers': {
                                    'color': '#056197',
                                    'visibility': 'off'
                                }
                            },
                            {
                                'featureType': 'subway',
                                'elementType': 'all',
                                'stylers': {
                                    'visibility': 'off'
                                }
                            },
                            {
                                'featureType': 'manmade',
                                'elementType': 'all',
                                'stylers': {
                                    'visibility': 'off'
                                }
                            },
                            {
                                'featureType': 'local',
                                'elementType': 'all',
                                'stylers': {
                                    'visibility': 'off'
                                }
                            },
                            {
                                'featureType': 'arterial',
                                'elementType': 'labels',
                                'stylers': {
                                    'visibility': 'off'
                                }
                            },
                            {
                                'featureType': 'boundary',
                                'elementType': 'geometry.fill',
                                'stylers': {
                                    'color': '#029fd4'
                                }
                            },
                            {
                                'featureType': 'building',
                                'elementType': 'all',
                                'stylers': {
                                    'color': '#1a5787'
                                }
                            },
                            {
                                'featureType': 'label',
                                'elementType': 'all',
                                'stylers': {
                                    'visibility': 'off'
                                }
                            }
                        ]
                    }
                },
                series: [
                    {
                        name: 'bikes',
                        type: 'scatter',
                        coordinateSystem: 'bmap',
                        data: snapshots[window.init_time],
                        symbolSize: function (val) {
                            return Math.max(val[2]/4, 5);
                        },
                        label: {
                            normal: {
                                formatter: '{b}',
                                position: 'right',
                                show: false
                            },
                            emphasis: {
                                show: true
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: function (val) {
                                    var diff = val['data'][3];
                                    if (diff > 0) {
                                        return '#FF3333';
                                    } else {
                                        return '#ddb926';
                                    }
                                }
                            }
                        }
                    }
                ]
            };
            chart.setOption(option);

            // 获取百度地图实例，使用百度地图自带的控件
            var bmap = chart.getModel().getComponent('bmap').getBMap();
            bmap.addControl(new BMap.MapTypeControl());

        });
        // 用于实时更新地图，响应用户操作
        var changeSnapshot = function () {
            var option = chart.getOption();
            var time = $('#map-wrap').data('time');
            option['series'][0]['data'] = snapshots[time]
            chart.setOption(option);
        }
    </script>
</body>
</html>
