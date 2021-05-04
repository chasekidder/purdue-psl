// Global Variables
var charts = [];



// Generate a Chart JS Config
function generateConfig(title, axis_label, labels){
    var datasets = []
        labels.forEach(function(label){
            datasets.push({
                label: label,
                fill: false,
                data: []
            });
        });

    var config = {
        type: 'line',
        labels: labels,
        title: title,
        axisLabel: axis_label,
        data: {
            datasets: datasets
        },
        options: {
            title: {
                display: true,
                text: title
            },
            scales: {
                xAxes: [{
                    type: 'realtime',
                    realtime: {
                        duration: 20000,
                        refresh: 1000,
                        delay: 2000,
                        onRefresh: onRefresh
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: axis_label
                    },
                    // ticks: {
                    //     min: -5,
                    //     max: 15
                    // }
                }]
            },
            plugins: {
                colorschemes: {
                    scheme: "tableau.Tableau10"
                }
            },
            
            
            
        }
    };
    return config;

}


        
// Show/Hide Function for Checkboxes
function showHide(id){
    let chart = document.getElementById("chart_" + id)

    if (document.getElementById("checkbox_" + id).checked){
        chart.style.visibility = 'visible';
        //chart.style.height = 400;
        charts[id].enabled = true;
    }
    else {
        chart.style.visibility = 'hidden';
        //chart.style.height = 0;
        charts[id].enabled = false;
    }
}


// Request Data Promise And Initialize Charts
function initCharts() {
    const url = "/api/";  
    fetch(url)
        .then((resp) => resp.json())
        .then(function(new_live_data) {
            live_data = new_live_data; 
            createCharts();  
        })
        .catch(function(error) {
            console.log(error);
        });

}



// Dynamically Create All Charts Based On API Response
function createCharts(){
    var parent = document.getElementById("chart_div");
    var chk_parent = document.getElementById("checkbox_div");
    var chart_num = 0;

    Chart.defaults.line.spanGaps = true;

    for (sensor in live_data){
        // Create New Checkbox
        var chk_div = document.createElement("div");
        chk_div.setAttribute("class", "form-check form-switch form-check-inline");

        var chk_input = document.createElement("input");
            chk_input.setAttribute("class", "form-check-input");
            chk_input.setAttribute("type", "checkbox");
            chk_input.setAttribute("id", "checkbox_" + chart_num);
            chk_input.setAttribute("onClick", "showHide(" + chart_num + ");");

        var chk_label = document.createElement("label");
            chk_label.setAttribute("class", "form-check-label");
            chk_label.setAttribute("for", "checkbox_" + chart_num);
            chk_label.innerHTML = live_data[sensor]["sensor"];

        // Append Checkbox Elements to DOM
        chk_div.appendChild(chk_input);
        chk_div.appendChild(chk_label);
        chk_parent.appendChild(chk_div);

        // Create New Chart Element
        var chart_element = document.createElement("canvas");
        chart_element.setAttribute("id", "chart_" + chart_num);
        chart_element.setAttribute("width", "400");
        chart_element.setAttribute("height", "400");

        parent.appendChild(chart_element);


        // Get Element Context
        var chart_elem = document.getElementById("chart_" + chart_num)
        chart_elem.style.visibility = "hidden";
        var ctx = chart_elem.getContext("2d");

        // Create Config
        config = generateConfig(live_data[sensor]["sensor"], 
                live_data[sensor]["type"] + " (" + live_data[sensor]["unit"] + ")", 
                [live_data[sensor]["type"]]);
            

        chart = new Chart(ctx, config);
        chart.config.dataset_id = chart_num;
        chart.enabled = false;

        // Append chart to global list
        charts.push(chart);

        chart_num = chart_num + 1;
    }
}



// Add New Data To Chart JS Dataset
function onRefresh(chart) {
    if (chart.enabled === true){
        chart.config.data.datasets.forEach(function(dataset) {
            for (sensor in live_data) {

                if (sensor == chart.config.dataset_id){
                    dataset.data.push({
                        // x: live_data[sensor]["timestamp"],
                        x: Date.now(),
                        y: live_data[sensor]["value"]
                    });
                }
            }
        });

        chart.update();
    }

}
