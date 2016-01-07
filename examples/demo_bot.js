/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          ______     ______     ______   __  __     __     ______
          /\  == \   /\  __ \   /\__  _\ /\ \/ /    /\ \   /\__  _\
          \ \  __<   \ \ \/\ \  \/_/\ \/ \ \  _"-.  \ \ \  \/_/\ \/
          \ \_____\  \ \_____\    \ \_\  \ \_\ \_\  \ \_\    \ \_\
           \/_____/   \/_____/     \/_/   \/_/\/_/   \/_/     \/_/


This is a sample Slack bot built with Botkit.

This bot demonstrates many of the core features of Botkit:

* Connect to Slack using the real time API
* Receive messages based on "spoken" patterns
* Send a message with attachments
* Send a message via direct message (instead of in a public channel)

# RUN THE BOT:

  Get a Bot token from Slack:

    -> http://my.slack.com/services/new/bot

  Run your bot from the command line:

    token=<MY TOKEN> node team_bot.js

# USE THE BOT:

  Find your bot inside Slack to send it a direct message.

  Say: "Hello"

  The bot will reply "Hello!"

  Say: "Attach"

  The bot will send a message with a multi-field attachment.

  Send: "dm"

  The bot will reply with a direct message.

  Make sure to invite your bot into other channels using /invite @<my bot>!

# EXTEND THE BOT:

  Botkit is has many features for building cool and useful bots!

  Read all about it here:

    -> http://howdy.ai/botkit

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/

var Botkit = require('../lib/Botkit.js');
var requestify = require('requestify'); 
var Brauhaus = require('brauhaus');
require('brauhaus-beerxml');

if (!process.env.token) {
  console.log('Error: Specify token in environment');
  process.exit(1);
}

var controller = Botkit.slackbot({
 debug: false,
});

controller.spawn({
  token: process.env.token
}).startRTM(function(err) {
  if (err) {
    throw new Error(err);
  }
});


controller.hears(['hello'],'direct_message,direct_mention,mention',function(bot,message) {
    bot.reply(message,"Hello.");
})

controller.hears(['attach'],'direct_message,direct_mention',function(bot,message) {

  var attachments = [];
  var attachment = {
    title: 'This is an attachment',
    color: '#FFCC99',
    fields: [],
  }

  attachment.fields.push({
    label: 'Field',
    value: 'A longish value',
    short: false,
  })

  attachment.fields.push({
    label: 'Field',
    value: 'Value',
    short: true,
  })

  attachment.fields.push({
    label: 'Field',
    value: 'Value',
    short: true,
  })

  attachments.push(attachment);

  bot.reply(message,{
    text: 'See below...',
    attachments: attachments,
  },function(err,resp) {
    console.log(err,resp);
  });
});

controller.hears(['dm me'],'direct_message,direct_mention',function(bot,message) {
  bot.startConversation(message,function(err,convo) {
    convo.say('Heard ya');
  });

  bot.startPrivateConversation(message,function(err,dm) {
    dm.say('Private reply!');
  })

});

controller.hears(['goodnight'], 'ambient', function(bot, message) {
	bot.reply(message, "Don't forget to count the hops jumping into the boil kettle!");
});

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}
function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

controller.on('file_share',function(bot,message) {
	var file_type = message.file.filetype;
	var file = message.file.url_download;
	if(file_type == 'xml') {
		requestify.get(file).then(function(response) {
		    // Get the response body (JSON parsed - JSON response or jQuery object in case of XML response)
			var beerxml = response.body;
			var xmlRecipes = Brauhaus.Recipe.fromBeerXml(beerxml);
			var xmlRecipe = xmlRecipes[0];
			xmlRecipe.calculate();
			var timeline = xmlRecipe.timeline(false);
			var b = JSON.stringify(timeline);
			var c = JSON.parse(b);
			// Send recipe to parse
			var jsondata = {
				"data": xmlRecipe,
				"general": {
					"color": xmlRecipe.color,
					"ibu": xmlRecipe.ibu,
					"og": xmlRecipe.og,
					"fg": xmlRecipe.fg,
					"abv": xmlRecipe.abv
					
				}
			}
			var options = {
				"headers" : {
			        'X-Parse-Application-Id': 'vqy28dkElsQiH8xlM8Yc69vpFjDfGTV4DAinWsjU',
			        'X-Parse-REST-API-Key': 'iI5MrD2b204dk0NE5xlG9sR1J3lkZWGfohXCnewj',
			        'X-Parse-Revocable-Session': 1,
			        'Content-Type': 'application/json'
			    },
			    "dataType": "json"
			};
			console.log(jsondata);
			requestify.post('https://api.parse.com/1/classes/recipe', {"data": jsondata}, options).then(function(response) {
				console.log(response);
				var color = Brauhaus.srmToRgb(xmlRecipe.color);
				var hex = rgbToHex(color[0], color[1], color[2]);
				var id = response.getBody().objectId;
				var url = 'http://share.tatx.us/recipe/' + id; 
				
				  var attachments = [];
				  var attachment = {
				    title: xmlRecipe.name,
				    text: xmlRecipe.style.name,
				    title_link: url,
				    color: hex,
				    fields: [],
				  }
				  	
				  attachment.fields.push({
				    title: 'ABV',
				    value: xmlRecipe.abv.toFixed(1) + ' %',
				    short: true,
				  })
				
				  attachment.fields.push({
				    title: 'IBU',
				    value: xmlRecipe.ibu.toFixed(1) + ' IBU',
				    short: true,
				  })
				  
				  attachment.fields.push({
				    title: 'OG',
				    value: xmlRecipe.og.toFixed(3),
				    short: true,
				  })
				  attachment.fields.push({
				    title: 'FG',
				    value: xmlRecipe.fg.toFixed(3),
				    short: true,
				  })		  		
				  attachments.push(attachment);
				  bot.reply(message,{
				    text: 'See below...',
				    attachments: attachments,
				  },function(err,resp) {
				    console.log(err,resp);
				  });				
			}, function(err) {
				console.log(err);
			});
			
			
			

		});
	}
});

controller.hears(['abv'],'direct_message,direct_mention,mention',function(bot,message) {
  var og = 0;
  var fg = 0;
  bot.startConversation(message,function(err,convo) {

    convo.ask('Whats the OG?',function(response,convo) {
		console.log(response.text);
		og = response.text;
		convo.next();
    });
    convo.ask('Whats the FG?', function(response, convo){
	   	var abv = (og - response.text)*131;
	   	var calc = abv.toFixed(1) + '%';
	   	convo.say('Cool, your estimated abv is ' + calc);
	   	convo.next(); 
    });


  });

});
function toTitleCase(str)
{
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}
controller.hears(['What hop can you substitute for (.*)'],'direct_message,direct_mention,mention',function(bot,message) {
	var matches = message.text.match(/^.*?\bhop\b.*?\bsubstitute\b.*?for(.*)/m);
  	var match = matches[1];
  	var name = match.replace(/\s+/g, '');
	requestify.get('http://brewerwall.com/api/v1/hops?name=' + name, {"dataType": "json"}).then(function(response){
		var results = response.getBody();
		var json = JSON.parse(results);
		var id = json[0].id;
		var text = '';
		var url = 'http://brewerwall.com/hops/';
		json.forEach(function(item, key){
			text += key + 1 + ') ' + toTitleCase(item.name) + ' (' + item.origin + ') \n';
		});
		bot.startConversation(message,function(err,convo) {
			convo.ask('Looks like there are ' + json.length + ' which one? \n' + text,function(response,convo) {
				var id = json[response.text - 1].id;
				requestify.get('http://brewerwall.com/api/v1/hops/' + id + '/substitutes').then(function(response){
					var results = response.getBody();
					var json = JSON.parse(results);
					var text = '';
					var size = json.length;
					json.forEach(function(item, key){

						text += '• <' + url + item.id + '|' + toTitleCase(item.name) + '>'
						
						if(key + 1 != size) {
							text += '\n';
						}
					});
					if(json.length == 0) {
						text += 'None, that hop is unique like a snowflake!';
					}
					  var attachments = [];
					  var attachment = {
					    title: 'Hop Substitions For ' + toTitleCase(name),
					    thumb_url: 'http://brewerwall.com/img/logo.png',
					    fields: [],
					  }
					  	
					  attachment.fields.push({
					    value: text,
					    short: false,
					  })
	  		
					  attachments.push(attachment);
					  bot.reply(message,{
					    attachments: attachments,
					  },function(err,resp) {
					    console.log(err,resp);
					  });	
				
					convo.next();
				}, function(err){
					console.log(err);
				});
				
			});
		});

		
	}, function(err){
		console.log(err);
	});
});
