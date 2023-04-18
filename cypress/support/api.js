const apiV1Url = `${Cypress.config('baseUrl')}/api/v1`
const headers = { authorization: Cypress.env('TOKEN') }

Cypress.Commands.add('apiGetValueStreams', () =>
  cy.request({ url: `${apiV1Url}/valueStreams`, headers }),
)

Cypress.Commands.add('apiGetTeams', () =>
  cy.request({ url: `${apiV1Url}/teams`, headers }),
)

Cypress.Commands.add('apiGetUsers', () => {
  cy.request({ url: `${apiV1Url}/users`, headers })
})

Cypress.Commands.add('apiGetTicketBoards', () => {
  cy.request({ url: `${apiV1Url}/ticketboards`, headers })
})

Cypress.Commands.add(
  'apiCreateValueStream',
  (valueStreamName, organizationId) =>
    cy.apiGetUsers().then(resp => {
      expect(resp.status).to.equal(200)
      const { result: users } = resp.body
      expect(users).length.gt(0)
      const [firstUser] = users
      cy.request({
        method: 'POST',
        url: `${apiV1Url}/valuestreams`,
        body: {
          name: valueStreamName,
          organizationId,
          userIds: [firstUser.id],
        },
        headers,
      }).then(resp => {
        expect(resp.status).to.equal(201)
        cy.wrap({ valuestream: resp.body })
      })
    }),
)

Cypress.Commands.add('apiDeleteValueStream', vsId =>
  cy.request({
    method: 'DELETE',
    url: `${apiV1Url}/valuestreams/${vsId}`,
    headers,
    failOnStatusCode: false,
  }),
)

Cypress.Commands.add('apiDeleteOrganization', orgId =>
  cy.request({
    method: 'DELETE',
    url: `${apiV1Url}/organizations/${orgId}`,
    headers,
    failOnStatusCode: false,
  }),
)

Cypress.Commands.add('apiDeleteTeam', teamId =>
  cy.request({
    method: 'DELETE',
    url: `${apiV1Url}/teams/${teamId}`,
    headers,
    failOnStatusCode: false,
  }),
)

Cypress.Commands.add('apiCreateOrganization', orgName =>
  cy.apiGetUsers().then(resp => {
    expect(resp.status).to.equal(200)
    const { result: users } = resp.body
    expect(users).length.gt(0)
    const [firstUser] = users
    cy.request({
      method: 'POST',
      url: `${apiV1Url}/organizations`,
      body: { name: orgName, userIds: [firstUser.id] },
      headers,
    }).then(resp => {
      expect(resp.status).to.equal(201)
      cy.wrap({ organization: resp.body })
    })
  }),
)
Cypress.Commands.add('apiCreateTeam', (teamName,collectorTargetIds, teamSize, valuestreamId) =>
  cy.apiGetUsers().then(resp => {
    expect(resp.status).to.equal(200)
    const { result: users } = resp.body
    expect(users).length.gt(0)
    const [firstUser] = users
    cy.request({
      method: 'POST',
      url: `${apiV1Url}/teams`,
      body: { name: teamName, userIds: [firstUser.id], collectorTargetIds: collectorTargetIds, teamSize:teamSize, valuestreamId: valuestreamId},
      headers,
    }).then(resp => {
      expect(resp.status).to.equal(201)
      cy.wrap({ team: resp.body })
    })
  }),
)

Cypress.Commands.add('apiUpdateTeam', (teamName,collectorTargetIds, teamSize, valuestreamId, teamId) =>
  cy.apiGetUsers().then(resp => {
    expect(resp.status).to.equal(200)
    const { result: users } = resp.body
    expect(users).length.gt(0)
    const [firstUser] = users
    cy.request({
      method: 'PUT',
      url: `${apiV1Url}/teams/${teamId}`,
      body: { name: teamName, userIds: [firstUser.id], collectorTargetIds: collectorTargetIds, teamSize:teamSize, valuestreamId: valuestreamId},
      headers,
    }).then(resp => {
      expect(resp.status).to.equal(200)
      cy.wrap({ team: resp.body })
    })
  }),
)

Cypress.Commands.add('apiGetAvailableTicketBoard', () => {
  cy.apiGetTeams().then(resp => {
    expect(resp.status).to.equal(200)
    const { result: teams } = resp.body
    expect(teams).length.gt(0)

    var activeCollectorTargets = []
    teams.forEach((team) => {
      activeCollectorTargets.push(...team.collectorTargets);
    });

    cy.apiGetTicketBoards().then(resp =>{
      expect(resp.status).to.equal(200)
      const { result: ticketBoards } = resp.body
      expect(ticketBoards).length.gt(0)
      var allBoards = []
      ticketBoards.forEach((board) => {
        allBoards.push(board.id);
      });
      const id = allBoards.find(boardId => !activeCollectorTargets.includes(boardId))
      cy.wrap({ id: id})
    })
  })
})
