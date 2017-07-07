/**
 * Created by Administrator on 2017/7/6.
 */
function logout() {
    window.open('/logout', "_self");
}

function run(element) {
    var num = number();
    if (num > 0){
        //$('#myModal').click();
        element.removeAttribute('data-target');
        var case_list = [];
        var eles = $('input[type="checkbox"]');
        for(var i=0; i<eles.length;i++){
            if (eles[i].checked){
                var case_name = eles[i].parentNode.nextElementSibling.innerHTML;
                case_list.push(case_name);

                //$.post("/delete_case", {'case_name': case_list}, "form").done(function(data){
                    // var value = JSON.parse(data);
                  //  if(data.status){
                    //    alert("删除成功!");
                      //  window.open("/case", "_self");
                    //}
                //})
            }

        }
        if(case_list.length){
            $.ajax({
                    url: "/run_case",
                    type: "POST",
                    data: JSON.stringify({
                        "case_name": case_list
                    }),
                    dataType: "json",
                    //traditional: true,
                    contentType: "application/json",
                    success: function(data){

                        document.write(data.html);
                    }
                    }
                );
        }

        $("#myModal").attr("aria-hidden", true);
        //$("#myModal").attr("data-dismiss", modal)
    }
    else{
        //alert("请至少选择一条用例!");
        element.setAttribute("data-target", "#myModal_alert");
    }





}
