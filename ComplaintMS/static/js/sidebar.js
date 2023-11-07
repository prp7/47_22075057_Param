let openSideBarE1 = document.getElementById('open-sidebar');
    const sidebarEl = document.getElementById('sdbar');
    const closeSidebarEl = document.getElementById('close-sidebar');
    const main_div = document.getElementById('main_div')
    openSideBarE1.addEventListener("click",() => {
        
        sidebarEl.style.transform = "translate(0px)";
        main_div.style.marginLeft = sidebarEl.style.width;

    })

    closeSidebarEl.addEventListener("click",()=>{
        sidebarEl.style.transform = "translate(-250px)";
        main_div.style.marginLeft = "0";
    })

    const btn=document.getElementById('bnt')
    const url=btn.getAttribute(href)