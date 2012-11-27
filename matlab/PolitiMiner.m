
clc

[stat,h1] = web('http://google.com');
h1.setVisible(false);


[stat,h1] = web('http://www.politifact.com/personalities/');

hStr = h1.getHtmlText;
hChar = hStr.toCharArray;

sStart = strfind(hChar,'Other people and groups');

