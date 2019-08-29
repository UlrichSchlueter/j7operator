var data = {
    "type": "timeline",
    "options": {
        // Depricated and will be removed in future. Please use elements.* instead.
        // "colorFunction": function(text, data, dataset, index) {
        //     return Color('black');
        // },
        // "showText": true,
        // "textPadding": 4
        "elements": {
            "colorFunction": function(text, data, dataset, index) {
                return Color('black');
            },
            "showText": true,
            "textPadding": 4
        }
    },
    "data": {
        "labels": [
            "Cool Graph",
             "Cool Graph1",
              "Cool Graph2",
            "heater1"
        ],
        "datasets": [
            {
                "data": [
                    [
                        "2018-01-22T16:00:00.000Z",
                        "2018-01-23T05:40:44.626Z",
                        "Unknown"
                    ]
                ]
            },
             {
                "data": [
                    [
                        "2018-01-22T16:00:00.000Z",
                        "2018-01-23T05:40:44.626Z",
                        "XXX"
                    ]
                ]
            },
             {
                "data": [
                    [
                        "2018-01-22T16:00:00.000Z",
                        "2018-01-23T05:40:44.626Z",
                        "XXX"
                    ]
                ]
            },
            {
                "data": [
                    [
                        "2018-01-22T16:00:00.000Z",
                        "2018-01-22T20:00:00.000Z",
                        "On"
                    ],
                    [
                        "2018-01-22T25:00:00.000Z",
                        "2018-01-23T04:57:55.437Z",
                        "Off"
                    ],
                    
                    [
                        "2018-01-23T04:57:55.437Z",
                        "2018-01-23T05:40:44.626Z",
                        "On"
                    ]
                ]
            }
        ]
    },
  };
  var ctx = document.getElementById('actionChart');
  var chart = new Chart(ctx, data);
  