export default function Filters({filters,setFilters}){

  const update=(k,v)=>{
   setFilters({...filters,[k]:v})
  }
 
   // Determine V/S text
  let vsText = "Last Month";
  if (filters.time_range === "Today") vsText = "Yesterday";
  if (filters.time_range === "Last 7 Days") vsText = "Previous 7 Days";
  if (filters.time_range === "Last 30 Days") vsText = "Previous 30 Days";

  return(
   <div className="sub-nav">
     <div className="filters">
       <select className="filter-select" value={filters.time_range} onChange={e=>update("time_range",e.target.value)}>
         <option>This Month</option>
         <option>Today</option>
         <option>Last 7 Days</option>
         <option>Last 30 Days</option>
       </select>
   
       <select className="filter-select" value={filters.channel} onChange={e=>update("channel",e.target.value)}>
         <option value="All Channels">All Channels</option>
         <option value="Mobile App">Mobile App</option>
         <option value="NetBanking">NetBanking</option>
         <option value="Branch Assisted">Branch Assisted</option>
       </select>
   
       <select className="filter-select" value={filters.region} onChange={e=>update("region",e.target.value)}>
         <option value="All Regions">All Regions</option>
         <option value="North Zone">North Zone</option>
         <option value="South Zone">South Zone</option>
         <option value="East Zone">East Zone</option>
         <option value="West Zone">West Zone</option>
       </select>

       <select className="filter-select" value={filters.segment} onChange={e=>update("segment",e.target.value)}>
         <option value="All Segments">All Segments</option>
         <option value="Retail">Retail</option>
         <option value="Priority">Priority</option>
         <option value="NR">NR</option>
         <option value="SME">SME</option>
       </select>
     </div>

     <div style={{display: "flex", gap: "12px", alignItems: "center"}}>
       <span style={{color: "#a0aec0", fontSize: "0.85rem"}}>V/S <span style={{color: "#fff"}}>{vsText}</span></span>
       <button className="export-btn">
         Export
         <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
       </button>
     </div>
   </div>
  )
 }
