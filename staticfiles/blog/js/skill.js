
	 $(function() {
function split( val ) {
return val.split( /,\s*/ );
}
function extractLast( term ) {
return split( term ).pop();
}
     
var projects = ['Advertising', 'Marketing', 'Public Relations', 'Publicity', 'Sales', 'Performance Advertising','Social Media Advertising','SEO','Digital Marketing','Social Media Influencer','Event Management','Hotel Management','Cooking','Catering','Intellectual Property Law','Estate Planning Law','Employment Law','Tax','Civil Litigaion','Data Entry','Import and Export','Architecture','Interior Design','Adobe Photoshop','Adobe Illustrator','Adobe InDesign','Adobe Animate','Corel Draw','Adobe Flash','AutoCad','Sketch','Autodesk','Inkscape','Adobe XD','Invision Studio','Animation','Graphic Design','Photo Editing','Entrepreneurship','Communication Skill','Leadership','Team Player','Accounting','Stock Marketing','Corporate Finance','Photography','Journalism','Content Writing','Blogging','Video Making','Acting','Music','Video Editing','Computer Networking','C','C++','Java','Javascript','Node.js','Angluar JS','Vue Js','Express JS','MySQL','PHP','HTML','CSS','Robotics','Ethical Hacking','Android app Development','Web Development','iOS Development','Wordpress','Python','R','Ruby on rails','React JS','React Native','C# Programming','MongoDB','Rest API','Internet Of Things','Data Science','Docker','AWS','Machine Learning','Block Chain','Django','App Development', 'Data Analytics','Dot .Net','C#.Net','Apache Cassandra','C++ Programming','C Programming','OpenCv','Image Processing','Deep Learning','Server Handling','Google Analytics','Creative Writing','Content Writing','Cybersecurity','Cloud Computing/AWS', 'Blockchain','Data Visualization','Flux','Java Development Kit','XML','Web Hosting','Software Architecture','AJAX','Web Scraping','Microcontroller','Microprocessor','Algorithm and Analyis','Electronic Design','Automotive','Electrical','Logo Design','Website Design','Illustrator','Game Development','Youtube'
      ];
     
$( "#id_skills_required" )
 // don't navigate away from the field on tab when selecting an item
.bind( "keydown", function( event ) {
if ( event.keyCode === $.ui.keyCode.TAB &&
$( this ).autocomplete( "instance" ).menu.active ) {
event.preventDefault();
}
})
.autocomplete({
minLength: 0,
source: function( request, response ) {
// delegate back to autocomplete, but extract the last term
response( $.ui.autocomplete.filter(
projects, extractLast( request.term ) ) );
},

//    source:projects,    
focus: function() {
// prevent value inserted on focus
return false;
},
select: function( event, ui ) {
var terms = split( this.value );
// remove the current input
terms.pop();
// add the selected item
terms.push( ui.item.value );
// add placeholder to get the comma-and-space at the end
terms.push( "" );
this.value = terms.join( ", " );
    
    var selected_label = ui.item.label;
    var selected_value = ui.item.value;
    
    var labels = $('#labels').val();
    var values = $('#values').val();
    
    if(labels == "")
    {
        $('#labels').val(selected_label);
        $('#values').val(selected_value);
    }
    else    
    {
        $('#labels').val(labels+","+selected_label);
        $('#values').val(values+","+selected_value);
    }   
    
return false;
}
});

 });     
