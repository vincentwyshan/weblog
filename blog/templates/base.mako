<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
    xmlns:tal="http://xml.zope.org/namespaces/tal">
    <head>
        <meta charset="utf-8"/>
        <title>
            <%block name="title">
            Blog | Vincent's Notes
            </%block>
        </title>

        <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
        <meta name="keywords" content="python web application" />
        <meta name="description" content="pyramid web application" />
        <link rel="shortcut icon"
        href="/static/favicon.ico" />
        <link href="/static/js/google-code-prettify/prettify.css" type="text/css" rel="stylesheet" />
        <link href="/static/css/bootstrap.css" rel="stylesheet"/>
        <script type="text/javascript" src="/static/js/google-code-prettify/prettify.js" ></script>

        <%block name="css">

        </%block>

        <%block name="js">

        </%block>
        <style type="text/css">
            /* Override some defaults */
            html, body {
                background-color: #eee;
            }
            body {
                padding-top: 40px; /* 40px to make the container go all the way to the bottom of the topbar */
            }
            .container > footer p {
                text-align: center; /* center align it with the container */
            }
            .container {
                width: 820px; /* downsize our container to make the content feel a bit tighter and more cohesive. NOTE: this removes two full columns from the grid, meaning you only go to 14 columns and not 16. */
            }

            /* The white background content wrapper */
            .container > .content {
                background-color: #fff;
                padding: 20px;
                margin: 0 -20px; /* negative indent the amount of the padding to maintain the grid system */
                -webkit-border-radius: 0 0 6px 6px;
                -moz-border-radius: 0 0 6px 6px;
                border-radius: 0 0 6px 6px;
                -webkit-box-shadow: 0 1px 2px rgba(0,0,0,.15);
                -moz-box-shadow: 0 1px 2px rgba(0,0,0,.15);
                box-shadow: 0 1px 2px rgba(0,0,0,.15);
            }

            /* Page header tweaks */
            .page-header {
                background-color: #f5f5f5;
                padding: 20px 20px 10px;
                margin: -20px -20px 20px;
            }

            /* Styles you shouldn't keep as they are for displaying this base example only */
            .content .span10,
            .content .span4 {
                min-height: 500px;
            }
            .span10 {
                border-right: 1px solid #eee;
            }
            /* Give a quick and non-cross-browser friendly divider */
            .content .span4 {
                margin-left: 0;
                padding-left: 19px;
            }
            .content {
                border-left: 1px solid #eee;
            }

            .topbar .btn {
                border: 0;
            }

        </style>
        <!-- <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js" /> -->
        </head>
        <body onload="prettyPrint()" >

            <div class="topbar">
                <div class="fill">
                    <div class="container">
                        <!-- <a class="brand" href="#">Home</a>
                        <a class="brand" href="#">About</a> -->
                        <ul class="nav">
                            %for post in toplist:
                            <li><a href="${post.id}">${post.title}</a></li>
                            %endfor
                        </ul>
                    </div>
                </div>
            </div>

            <div class="container">
                <div class="content">
                    <div class="page-header">
                        <%block name="header">
                        <h1>VINCENT Blog</h1>
                        </%block>

                    </div>

                    <div class="row">
                            ${self.body()}
                    </div>
                </div>
                <footer>
                <%block name="footer">
                <p>© Copyright 2011 by Vincent Wen.</p>
                </%block>
                </footer>


            </div>

        </body>
    </html>

