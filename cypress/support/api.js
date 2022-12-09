const apiUrl = `${Cypress.config('baseUrl')}/api/v1`

const headers = { authorization: Cypress.env('TOKEN') }

Cypress.Commands.add('apiGetValueStreams', () =>
  cy.request({ url: `${apiUrl}/valueStreams`, headers }),
)

Cypress.Commands.add('apiGetTeams', () =>
  cy.request({ url: `${apiUrl}/teams`, headers }),
)

Cypress.Commands.add(
  'apiCreateValueStream',
  (valueStreamName, organizationId) =>
    cy
      .request({
        method: 'POST',
        url: `${apiUrl}/valuestreams`,
        body: {
          name: valueStreamName,
          organizationId,
        },
        headers,
      })
      .then(resp => {
        expect(resp.status).to.equal(201)
        cy.wrap({ valuestream: resp.body })
      }),
)

Cypress.Commands.add('apiDeleteValueStream', vsId =>
  cy.request({
    method: 'DELETE',
    url: `${apiUrl}/valuestreams/${vsId}`,
    headers,
  }),
)

Cypress.Commands.add('apiDeleteOrganization', orgId =>
  cy.request({
    method: 'DELETE',
    url: `${apiUrl}/organizations/${orgId}`,
    headers,
  }),
)

Cypress.Commands.add('apiDeleteTeam', teamId =>
  cy.request({
    method: 'DELETE',
    url: `${apiUrl}/dashboard/${teamId}`,
    headers,
  }),
)

Cypress.Commands.add('apiCreateOrganization', orgName =>
  cy
    .request({
      method: 'POST',
      url: `${apiUrl}/organizations`,
      body: { name: orgName },
      headers,
    })
    .then(resp => {
      expect(resp.status).to.equal(201)
      cy.wrap({ organization: resp.body })
    }),
)