$(document).ready(function() {
    $('#search-btn').click(function() {
        var keyword = $('#keyword').val();
        var start_date = $('#start_date').val();
        var end_date = $('#end_date').val();
        $.ajax({
            url: '/search/',
            type: 'POST',
            data: {
                'keyword': keyword,
                'start_date': start_date,
                'end_date': end_date,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(result) {
                $('#search-result tbody').empty();
                for (var i = 0; i < result.length; i++) {
                    var row = $('<tr>');
                    row.append($('<td>').text(result[i].content));
                    row.append($('<td>').text(result[i].like));
                    row.append($('<td>').text(result[i].comment));
                    row.append($('<td>').text(result[i].search_time));
                    $('#search-result tbody').append(row);
                }
            },
            error: function(xhr, status, error) {
                alert(xhr.responseText);
            }
        });
    });
});