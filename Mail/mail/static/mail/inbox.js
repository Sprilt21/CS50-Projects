let toReply = null;
//let replyButton = null;

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => {
    
    console.log(1);
    compose_email(null);
  });

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(mail) {

  // Show compose view and hide other views
  document.querySelector('#view-single').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  if (mail == null) {

    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  } else {

    console.log(4);

    document.querySelector('#compose-recipients').value = mail.sender;

    if(!mail.subject.includes("Re:")) {

      document.querySelector('#compose-subject').value = 'Re: ' + mail.subject;
    } else {

      document.querySelector('#compose-subject').value = mail.subject;
    }

    document.querySelector('#compose-body').value = 'On ' + mail.timestamp + ' ' + mail.sender + " wrote: " + mail.body + '\n';
  }

  document.querySelector('#compose-form').onsubmit = () => {

    fetch('/emails', {

      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {

      load_mailbox('sent');
      console.log(result);
    });

    return false;
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-single').style.display = 'none';
  /*document.querySelector('#archive').style.display = 'none';
  document.querySelector('#unarchive').style.display = 'none';*/

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch('/emails/' + mailbox, {
    method: 'GET',
    headers: {
      'accept-encoding': 'none',
      'content-type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(emails => {
      
      var emailBox = document.querySelector('#emails-view');

      emails.forEach(mail => {
        
        toReply = mail;

        //button.removeEventListener('click', clickEvent.bind(this));

        const element = document.createElement('div');
        element.id = 'email';

        const table = document.createElement('dl');

        const tableLeft = document.createElement('dt');
        tableLeft.innerHTML = mail.sender + '&nbsp;&nbsp;&nbsp;' + mail.subject;
        table.append(tableLeft);

        const tableRight = document.createElement('dd');
        tableRight.innerHTML = mail.timestamp;
        table.append(tableRight);

        if(mail.read) {
          element.className += "readEmail";
        } else {
          element.className += "unreadEmail";
        }

        element.append(table);

        element.addEventListener('click', function() {
          document.querySelector('#view-single').innerHTML = '';

          const arcButton = document.createElement('button');
          arcButton.className = "btn btn-sm btn-outline-primary";
          arcButton.innerHTML = 'Archive Email';
          arcButton.id = 'archive';
  
          const unarcButton = document.createElement('button');
          unarcButton.className = "btn btn-sm btn-outline-primary";
          unarcButton.innerHTML = 'Unarchive Email';
          unarcButton.id = 'unarchive';
  
          const replyButton = document.createElement('button');
          replyButton.className = "btn btn-sm btn-outline-primary";
          replyButton.innerHTML = 'Reply to Email';
          replyButton.id = 'reply';

          console.log('is mail read: ' + mail.read);
          console.log('mail id: ' + mail.id);
          
          if (!mail.read) {
           fetch('/emails/' + mail.id, {
              method: 'PUT',
              body: JSON.stringify({
                read: true
             })
           });
          }

          emailBox.style.display = 'none';
          document.querySelector('#compose-view').style.display = 'none';
          document.querySelector('#view-single').style.display = 'block';

          const emailInfo = document.createElement('div');

          emailInfo.innerHTML = `<strong>`+"From: "+`</strong>` + mail.sender
          + `<br>` +`<strong>`+"To: "+`</strong>`+ mail.recipients
          + `<br>` + `<strong>`+"Subject: "+`</strong>` + mail.subject
          + `<br>` + `<strong>`+"Timestamp: "+`</strong>` + mail.timestamp
          + `<br>`;

          document.querySelector('#view-single').appendChild(emailInfo);

          document.querySelector('#view-single').appendChild(replyButton);

          document.getElementById('reply').addEventListener('click', () => {
            compose_email(mail);
          });

          console.log(arcButton);
          console.log(unarcButton);

          document.querySelector('#view-single').appendChild(arcButton);
          document.querySelector('#archive').addEventListener('click', () => {

            console.log('archived');
            fetch('/emails/' + toReply.id, {
              
              method: 'PUT',
              body: JSON.stringify({
                archived: true
              })
            });

            load_mailbox('inbox');
          });

          document.querySelector('#view-single').appendChild(unarcButton);
          document.querySelector('#unarchive').addEventListener('click', () => {

            console.log('unarchive');
            fetch('/emails/' + toReply.id, {
              
              method: 'PUT',
              body: JSON.stringify({
                archived: false
              })
            });

            load_mailbox('inbox');
          });
          
          if(mailbox != 'sent') {
            if (mail.archived == true) {

              arcButton.style.display = 'none';
              unarcButton.style.display = 'block';
              //console.log(1);
              console.log('unarcbutton' + unarcButton);
            } else {
  
              arcButton.style.display = 'block';
              unarcButton.style.display = 'none';
              //console.log(2);
              console.log('arcbutton' + arcButton);
            }
          } else {
            arcButton.style.display = 'none';
            unarcButton.style.display = 'none';
          }

          console.log('element.addeventlistener' + document.getElementById('reply'));

          const emailBody = document.createElement('div');
          emailBody.innerHTML = `<br><br>` + mail.body;
          
          document.querySelector('#view-single').append(emailBody);
        });

        emailBox.append(element);
      });

      console.log(emails);
  });
}

function clickEvent() {

  return function() {

    compose_email(toReply);
  }
}
