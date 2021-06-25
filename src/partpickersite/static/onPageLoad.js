const csrftoken = Cookies.get('csrftoken');
var table_data = []
var num_items = 0
//creates the table for all of the parts using datatables
function load_table(racks_json){
    $(document).ready(function(){
        table = $('#racks_table').DataTable({
            scrollY: '500px',
            scrollCollapse: false,
            select: 'row',
            multiselect: true,
            data: table_data,
            order: [[4, 'asc']],
            paging: false,
            columns: [
            { title: "Part Number" },
            { title: "Description" },
            { title: "Location" },
            { title: "IP" },
            { title: "ID" }]
        });
        //creates a table for the selected parts
        checkout_table = $('#checkout_table').DataTable({
            scrollY: '500px',
            scrollCollapse: false,
            select: 'row',
            multiselect: true,
            data: [],
            order: [1, 'asc'],
            paging: false,
            dom: 'Bfrtip',
            buttons: [{
            text: 'Find Items',
            action: function ( e, dt, node, config ) {
                checkout();
            }}],
            columns: [
            { title: "Part Number" },
            { title: "Description" }],
        });
        checkout_table.clear();

        //adds the part to the checkout table when it is selected
        table.on('select', function(e, dt, type, indexes){
            if(type === 'row'){
                rows= table.rows('.selected').data();
                for(i=0; i < rows.length; i++){
                    if((rows[i][4] - 1) == indexes[0]){
                    selected_row = [rows[i][0], rows[i][1], rows[i][2], rows[i][3], rows[i][4]];
                }};
                checkout_table.row.add(selected_row).draw();
        }});
        //removes the part from the checkout table when deselected
        table.on('deselect', function(e, dt, type, indexes){
                if(type === 'row'){
                row_index = parseInt(table.rows(indexes)[0]) + 1;
                for(I=0; I < checkout_table.rows().data().length;I++){
                    checkout_row = checkout_table.row(I).data()[4];
                    if(row_index == checkout_row){
                        checkout_table.row(I).remove().draw();
                        break;
                }};
        }});
        //removes the part from the checkout table when it is selected
        checkout_table.on('select', function(e, dt, type, indexes){
            if(type === 'row'){
                row_to_deselect_index = checkout_table.rows(indexes).data()[0][4];
                console.log(row_to_deselect_index, indexes)
                checkout_table.row(checkout_table.rows(indexes)[0]).remove().draw();

                table.row(row_to_deselect_index  - 1).deselect();

        }});
    });
};
function checkout(){
    part_dictionary = [];
    part_numbers = []
    for(i=0; i < checkout_table.rows().data().length;i++){
        part_dictionary[i] = checkout_table.rows().data()[i];
        part_numbers[i] = checkout_table.rows().data()[i][4];
    };
        $.ajaxSetup({
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }});

//sends a post request with the data for the parts in the checkout table
    $.ajax({
        type: "POST",
        data: {'parts':JSON.stringify(part_dictionary)},
        dataType: "json",
        url: "map",
        complete: function(response){
        url_data = String(response.responseText)
        url_data = encodeURI(url_data)
        console.log(url_data)
        document.location =`map/${url_data}`

        }
    }).done(function (res) {
    });


    //console.log(part_numbers)
    //document.location = `map/${test}`

};
