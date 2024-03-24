Stanza(function(stanza, params) {
    const q = stanza.query({
      endpoint: 'http://localhost:8890/sparql',
      template: 'stanza.rq',
      parameters: params
    });

    q.then(function(data) {
      const rows = data.results.bindings;
      stanza.render({
        template: 'stanza.html',
        parameters: { rows: rows }
      });
  });
});
