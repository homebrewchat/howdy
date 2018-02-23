require('brauhaus-beerxml');
var express = require('express');
var app     = express();
var Botkit = require('./lib/Botkit.js');
var requestify = require('requestify');
var Brauhaus = require('brauhaus');
var Twitter = require('twitter');
var node_env = 'development';

app.set('port', (process.env.PORT || 3000));

//For avoidong Heroku $PORT error
app.get('/', function(request, response) {
    var result = 'App is running'
    response.send(result);
}).listen(app.get('port'), function() {
    console.log('App is running, server is listening on port ', app.get('port'));
});

var client = new Twitter({
  consumer_key: process.env.TWITTER_CONSUMER_KEY,
  consumer_secret: process.env.TWITTER_CONSUMER_SECRET,
  access_token_key: process.env.TWITTER_ACCESS_TOKEN_KEY,
  access_token_secret: process.env.TWITTER_ACCESS_TOKEN_SECRET,
});

if (!process.env.SLACK_TOKEN) {
  console.log('Error: Specify SLACK_TOKEN as environment variable');
  process.exit(1);
}

if (process.env.BOTKIT_DEBUG) {
  debug_enable = true;
} else {
  debug_enable = false;
}

var controller = Botkit.slackbot({
 debug: debug_enable,
});

controller.spawn({
  token: process.env.SLACK_TOKEN
}).startRTM(function(err) {
  if (err) {
    throw new Error(err);
  }
});

controller.on('create_bot', function() {
  controller.say(
    {
      text: 'I\'m back baby!',
      channel: 'C8TTK8Y58' // #bot_stuff
    }
  );
});


controller.hears(['help'],'direct_message,direct_mention,mention',function(bot,message) {
    bot.reply(message,"hello\ngoodnight\nWhat hops can I substitute for <hop>\nabv");
})

controller.hears(['hello'],'direct_message,direct_mention,mention',function(bot,message) {
    bot.reply(message,"Hello.");
})

controller.hears(['goodnight'], 'ambient', function(bot, message) {
	bot.reply(message, "Don't forget to count the hops jumping into the boil kettle!");
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

controller.hears(['[wW]hat hops? can (you|I) sub(stitute)? for (.*)'],'direct_message,direct_mention,mention,ambient',function(bot,message) {
	var matches = message.text.match(/^.*?\bhops?\b.*?\bsub(stitute)?\b.*?for([ \w]*)\??$/m);
  var match = matches[2];
  var name = match.replace(/\s+/g, '');
	requestify.get('http://www.brewerwall.com/api/v1/hops?name=' + name, {"dataType": "json"}).then(function(response){
		var results = response.getBody();
		var json = JSON.parse(results);
		var id = json[0].id;
		var text = '';
		var url = 'http://www.brewerwall.com/hops/';
		json.forEach(function(item, key){
			text += key + 1 + ') ' + toTitleCase(item.name) + ' (' + item.origin + ') \n';
		});
		bot.startConversation(message,function(err,convo) {
			convo.ask('Looks like there are ' + json.length + ' which one? \n' + text,function(response,convo) {
				var id = json[response.text - 1].id;
				var selectedHop = json[response.text - 1].name;
				requestify.get('http://www.brewerwall.com/api/v1/hops/' + id + '/substitutes').then(function(response){
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
					    title: 'Hop Substitions For ' + toTitleCase(selectedHop),
					    thumb_url: 'http://www.brewerwall.com/img/logo.png',
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

controller.hears(['tweet (.*)'],'direct_message,direct_mention,mention',function(bot,message) {
	console.log(message);
	if(message.channel == 'G0GP0PS67') {
		var matches = message.text.match(/tweet([\s\S]*)/m);
		var tweet_text = matches[1];
		client.post('statuses/update', {status: tweet_text},  function(error, tweet, response){
		  if(error) throw error;
		  var id = tweet.id_str;
		  var user = tweet.user.screen_name;
		  var url = 'https://twitter.com/' + user + '/status/' + id + '';
		  bot.reply(message,'I did it! \n' + url);
		});
	}
});

function toTitleCase(str)
{
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}
