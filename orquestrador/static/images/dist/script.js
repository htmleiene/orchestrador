const tl = new TimelineMax({repeat: -1});

tl.add('oval-bot-shrink');
tl.to('.oval-bot', .5, { attr: { width: '100' }});

tl.add('oval-right-grow-and-shrink');
tl.to('.oval-right', .5, { attr: { height: 250 }})
  .to('.oval-right', 0, { attr: {transform: 'scale(1,-1) translate(0,-275)'}})
  .to('.oval-right', .5, { attr: { height: 100 }})

tl.add('oval-top-grow-and-shrink');
tl.to('.oval-top', .5, { attr: { width: 250 }})
  .to('.oval-top', 0, { attr: {transform: 'scale(-1,1) translate(-275)'}})
  .to('.oval-top', .5, { attr: { width: 100 }})

tl.add('oval-left-grow-and-shrink');
tl.to('.oval-bot', 0, { attr: { transform: 'rotate(180 62.5 212.5)' }})
  .to('.oval-bot', 0.5, {attr: { height: 250 }})
  .to('.oval-left', 0, {height: 250}) 
  .to('.oval-left', 0, {autoAlpha: 1})
  .to('.oval-bot', 0, {autoAlpha: 0})
  .to('.oval-left', .5, {height: 100}) 

tl.add('oval-bot-grow')
tl.to('.oval-right', 0, {translate: '', attr: {transform: 'rotate(180 212.5 212.5) translate(0 150)'}})
  .to('.oval-right', .5, {attr: {width: 250}})