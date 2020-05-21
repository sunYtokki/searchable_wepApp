
$(document).ready(function(){

    result.forEach(elem => add_link(elem))

    function add_link(elem){
        let id = elem.id
        let jq = '#search'+id
        let url= window.location.search +'/view/'+id
        $(jq).attr("href", url)
    }

    //console.log(key)
    // var search_key = JSON.stringify(key)
    // console.log(search_key)
    // var searchregexp = new RegExp(search_key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), "gi");


    // var search_regexp = new RegExp(search_key, "g")
    // $(this).html($(this).html().replace(searchregexp,"<span class = 'highlight'>"+search_key+"</span>"))
    
     console.log(result)
    // console.log(element.innerHTML)

    $('#search_input').focus()

})
