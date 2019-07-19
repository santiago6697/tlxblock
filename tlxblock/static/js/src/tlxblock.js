/* Javascript for TrafficLightXBlock. */
function TrafficLightXBlock(runtime, element) {

    function updateTrafficLight(result) {
        var due_date = new Date(result.due_date);
        $('.due_date', element).text(due_date.toString());
        // $('.delta', element).text(result.delta);

        // These conditionals will handle CSS
        if (result.delta > 1814400) {
            // Condition for green light    
            $('.delta', element).text("more than 3 weeks");
            $('#snackbar', element).css("background-color", "green");
        } else if ((result.delta <= 1814400) && (result.delta >= 604800)) {
            // Condition for yellow light
            $('.delta', element).text("between 1 and 3 weeks");
            $('#snackbar', element).css("background-color", "yellow");
            $('#snackbar', element).css("color", "black");
        } else if (result.delta < 604800) {
            // Condition for red light
            $('.delta', element).text("less than 1 week");
            $('#snackbar', element).css("background-color", "red");
        } else {
            // Default resolution: No delta may be available, check Python script
            $('#snackbar', element).css("background-color", "blue");
        }
        myFunction();
    }

    // var handlerUrl = runtime.handlerUrl(element, 'increment_count');

    // $('p', element).click(function(eventObject) {
    //     $.ajax({
    //         type: "POST",
    //         url: handlerUrl,
    //         data: JSON.stringify({"hello": "world"}),
    //         success: updateCount
    //     });
    // });

    var handlerUrl = runtime.handlerUrl(element, 'traffic_light');

    $("document").ready(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"hello": "world"}),
            success: updateTrafficLight
        });
    });

    $(function ($) {
        /* Here's where you'd do things on page load. */
    });
}

function myFunction() {
    var snackbar = document.getElementById("snackbar");
    snackbar.className = "show";
    setTimeout(function(){ snackbar.className = snackbar.className.replace("show", ""); }, 10000);
  }