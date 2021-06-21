
	 $(function() {
function split( val ) {
return val.split( /,\s*/ );
}
function extractLast( term ) {
return split( term ).pop();
}
     
var projects = ['Full Stack Website Developer','Wordpress Developer','Website Builder & CMS','Game Developer','Development For Streamers','Web Programmer','Mobile App Developer','Desktop App Developer','Cybersecurity & Data Protector','Support & IT','Chatbot Developer','Databse Handler','User Testing','Logo Designer','UI & UX Designer','Game Designer','Graphic Designer','Business Card & Stationery Designer','Machine Learning Programmer','Resume Designer','Brochure Designer','Poster Designer','Flyer Designer','Book Designer','Tattoo Designer','Architecture & Interior Designer','Merchandise Designer','Social Media Advertiser','Social Media Marketer','SEO','Public Relations','SEM','Web Traffics','Article & Blog Posts','Translator','Podcast Writer','Copywriting','Video Editor','Short Video Ads','Animated GIFs Maker','Character Animator','Visual Effects Maker','Photographer','Voice Over Artist','Mixing & Mastering','Singer & Vocalist','Songwriter','Sound Designer','Script Writer','Vocal Tuning','DJ','Radio Jockey','Virtual Assistant','Data Entry','Market Researcher','Business Planner','SMM - Social Media Marketing','Customer Service & Support','Business Support','Technical Support','YouTuber','Pinterest','Linkedin','Jingles Maker','Backend Developer','Frontend Developer'
      ];
     
$( "#id_professional_title" )
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
