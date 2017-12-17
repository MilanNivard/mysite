(function() {
    var notesOffset = 0;

    var blackKeys = {
        1: 1,
        3: 3,
        6: 1,
        8: 2,
        10: 3
    };
    $.each(blackKeys, function(k, v) {
        blackKeys[k] = ' black black'+v;;
    });

    function blackKeyClass(i) {
        return blackKeys[(i % 12) + (i < 0 ? 12 : 0)] || '';
    }

    var $keys = $('<div>', {'class': 'keys'}).appendTo('#piano');

    var buildingPiano = false;

    var isIos = navigator.userAgent.match(/(iPhone|iPad)/i);

    function buildPiano() {
        if (buildingPiano) return;
        buildingPiano = true;

        $keys.trigger('build-start.piano');
        $keys.empty().off('.play');

        function addKey(i) {
            var dataURI = isIos ? '' : Notes.getDataURI(i);

            // trick to deal with note getting hit multiple times before finishing...
            var sounds = [
                new Audio(dataURI),
                new Audio(dataURI),
                new Audio(dataURI)
            ];
            var curSound = 0;
            var pressedTimeout;
            dataURI = null;
            function play(evt) {
                // sound
                sounds[curSound].pause();
                try {
                    sounds[curSound].currentTime = 0.001; //HACK - was for mobile safari, but sort of doesn't matter...
                } catch (x) {
                    console.log(x);
                }
                sounds[curSound].play();
                curSound = ++curSound % sounds.length;

                var $k = $keys.find('[data-key='+i+']').addClass('pressed');

                //TODO - it'd be nice to have a single event for triggering and reading
                $keys.trigger('played-note.piano', [i, $k]);

                // visual feedback
                window.clearTimeout(pressedTimeout);
                pressedTimeout = window.setTimeout(function() {
                    $k.removeClass('pressed');
                }, 200);
            }
            $keys.on('note-'+i+'.play', play);
            var $key = $('<div>', {
                'class': 'key' + blackKeyClass(i),
                'data-key': i,
                mousedown: function(evt) { $keys.trigger('note-'+i+'.play'); }
            }).appendTo($keys);
        }

        // delayed for-loop to stop browser from crashing :'(
        // go slower on Chrome...
        var i = -12, max = 17, addDelay = /Chrome/i.test(navigator.userAgent) ? 80 : 0;
        (function go() {
            addKey(i + notesOffset);
            if (++i < max) {
                setTimeout(go);
            } else {
                buildingPiano = false;
                $keys.trigger('build-done.piano');
            }
        })();
    }

    buildPiano();


     //
    // Setup keyboard interaction
    //

    var keyNotes = {
        /*a*/ 65: 0, // c
        /*w*/ 87: 1, // c#
        /*s*/ 83: 2, // d
        /*e*/ 69: 3, // d#
        /*d*/ 68: 4, // e
        /*f*/ 70: 5, // f
        /*t*/ 84: 6, // f#
        /*g*/ 71: 7, // g
        /*y*/ 89: 8, // g#
        /*h*/ 72: 9, // a
        /*u*/ 85: 10, // a#
        /*j*/ 74: 11, // b
        /*k*/ 75: 12, // c
        /*o*/ 79: 13, // c#
        /*l*/ 76: 14, // d
        /*p*/ 80: 15, // d#
        /*;*/ 186: 16, // e
        /*;*/ 59: 16, // e ... gotta figure out why it's sometimes 186 and sometimes 59
        /*,*/ 222: 17, // f
        /*]*/ 221: 18, // f#
        /*enter*/ 13: 19 // g
    };
    var notesShift = -12;
    var downKeys = {};

    function isModifierKey(evt) {
        return evt.metaKey || evt.shiftKey || evt.altKey;
    }

    $(window).keydown(function(evt) {
        var keyCode = evt.keyCode;
        // prevent repeating keys
        if (!downKeys[keyCode] && !isModifierKey(evt)) {
            downKeys[keyCode] = 1;
            var key = keyNotes[keyCode];
            if (typeof key != 'undefined') {
                $keys.trigger('note-'+(key+notesShift+notesOffset)+'.play');
                evt.preventDefault();
            } else if (evt.keyCode == 188) {
                notesShift = -12;
            } else if (evt.keyCode == 190) {
                notesShift = 0;
            } else if (keyCode == 37 || keyCode == 39) {
                notesOffset += (keyCode == 37 ? -1 : 1) * 12;
                buildPiano();
            }
        }
    }).keyup(function(evt) {
        delete downKeys[evt.keyCode];
    });

    // prevent quick find...
    $(window).keydown(function(evt) {
        if (evt.target.nodeName != 'INPUT' && evt.target.nodeName != 'TEXTAREA') {
            if (evt.keyCode == 222) {
                evt.preventDefault();
                return false;
            }
        }
        return true;
    });

 
})();
