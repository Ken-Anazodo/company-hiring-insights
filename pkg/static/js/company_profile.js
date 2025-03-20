
document.addEventListener("DOMContentLoaded", function () {
    var rolesChart = echarts.init(document.getElementById("roles-chart"));
    var citiesChart = echarts.init(document.getElementById("cities-chart"));

    rolesChart.setOption({
        title: { text: "Job Roles Distribution", left: "center" },
        tooltip: { trigger: "axis" },
        xAxis: { type: "category", data: rolesData.map((item) => item.name) },
        yAxis: { type: "value" },
        series: [{ name: "Job Roles", type: "bar", data: rolesData.map((item) => item.value), itemStyle: { color: "black" } }],
    });

    citiesChart.setOption({
        title: { text: "Job Postings by City", left: "center" },
        tooltip: { trigger: "item" },
        xAxis: { type: "category", data: citiesData.map((item) => item.name), axisLabel: { rotate: 30 } },
        yAxis: { type: "value", name: "Job Postings" },
        series: [{
            name: "Job Postings",
            type: "scatter",
            symbolSize: (val) => val[1] / 50,
            data: citiesData.map((item) => [item.name, item.value]),
            itemStyle: { color: "black" },
        }],
    });

 
    document.getElementById("company-select").addEventListener("change", function () {
        var selectedCompany = this.value;
        window.location.href = "/company/" + encodeURIComponent(selectedCompany);
    });
});
