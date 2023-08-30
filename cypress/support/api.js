Cypress.Commands.add('apiGetValueStreams', () =>
  cy.request({ url: '/api/v2/valueStreams', headers: {
      authorization: Cypress.env('token')
    }
  }),
)

Cypress.Commands.add('apiGetTeams', () =>
  cy.request({ url: '/api/v2/teams', headers: {
      authorization: Cypress.env('token')
    }
  }),
)

Cypress.Commands.add('apiGetUsers', () => {
  cy.request({ url: '/api/v2/users', headers: {
      authorization: Cypress.env('token')
    } 
  })
})

Cypress.Commands.add('apiGetTicketBoards', () => {
  cy.request({ url: '/api/v2/ticketboards', headers: {
      authorization: Cypress.env('token')
    }
  })
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
        url: '/api/v2/valuestreams',
        body: {
          name: valueStreamName,
          organizationId,
          userIds: [firstUser.id],
        },
        headers: {
          authorization: Cypress.env('token')
        },
      }).then(resp => {
        expect(resp.status).to.equal(201)
        cy.wrap({ valuestream: resp.body })
      })
    }),
)

Cypress.Commands.add('apiDeleteValueStream', vsId =>
  cy.request({
    method: 'DELETE',
    url: `/api/v2/valuestreams/${vsId}`,
    headers: {
      authorization: Cypress.env('token')
    },
    failOnStatusCode: false,
  }),
)

Cypress.Commands.add('apiDeleteOrganization', orgId =>
  cy.request({
    method: 'DELETE',
    url: `/api/v2/organizations/${orgId}`,
    headers: {
      authorization: Cypress.env('token')
    },
    failOnStatusCode: false,
  }),
)

Cypress.Commands.add('apiDeleteTeam', teamId =>
  cy.request({
    method: 'DELETE',
    url: `/api/v2/teams/${teamId}`,
    headers: {
      authorization: Cypress.env('token')
    },
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
      url: '/api/v2/organizations',
      body: { name: orgName, userIds: [firstUser.id] },
      headers: {
        authorization: Cypress.env('token')
      },
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
      url: '/api/v2/teams',
      body: { name: teamName, userIds: [firstUser.id], collectorTargetIds: collectorTargetIds, teamSize:teamSize, valuestreamId: valuestreamId},
      headers: {
        authorization: Cypress.env('token')
      },
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
      url: `/api/v2/teams/${teamId}`,
      body: { name: teamName, userIds: [firstUser.id], collectorTargetIds: collectorTargetIds, teamSize:teamSize, valuestreamId: valuestreamId},
      headers: {
        authorization: Cypress.env('token')
      },
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

    const activeCollectorTargetsIds = teams.flatMap(team => team.collectorTargets)
    const activeCollectorTargetIdsTable = {}
    for (const id of activeCollectorTargetsIds){
      activeCollectorTargetIdsTable[id] = true
    }

    cy.apiGetTicketBoards().then(resp =>{
      expect(resp.status).to.equal(200)
      const { result: ticketBoards } = resp.body
      expect(ticketBoards).length.gt(0)
      const inActiveBoard = ticketBoards.find(board => !(board.id in activeCollectorTargetIdsTable))
      cy.wrap({ id: inActiveBoard.id})
    })
  })
})
