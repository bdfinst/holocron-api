/* eslint-disable no-undef */
// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

const baseUrl = Cypress.config('baseUrl')
const timeout = 240000

Cypress.Commands.add('apiSetUp', (organizationName, valueStreamName) =>
  cy.apiCreateOrganization(organizationName).then(({ organization }) => {
    cy.apiCreateValueStream(valueStreamName, organization.id).then(
      ({ valuestream }) => {
        cy.wrap({
          organization,
          valuestream,
        })
      },
    )
  }),
)

Cypress.Commands.add('apiSafeDelTeam', teamId => {
  cy.apiGetTeams().then(({ body: { result: teams } }) => {
    const foundTeam = teams.find(team => team.id === teamId)
    if (foundTeam) {
      return cy.apiDeleteTeam(teamId)
    }
    // don't care if the team is already deleted on the test
    return cy.wrap({})
  })
})

Cypress.Commands.add(
  'apiTearDown',
  (createdTeamId, organization, valueStream) => {
    cy.apiSafeDelTeam(createdTeamId).then(() => {
      cy.apiDeleteValueStream(valueStream.id).then(() => {
        cy.apiDeleteOrganization(organization.id)
      })
    })
  },
)

Cypress.Commands.add('visitDashboard', () => {
  cy.intercept('GET', '**/api/v1/users').as('getUsers')
  cy.intercept('GET', '**/api/v1/teams').as('getTeams')
  cy.intercept('GET', '**/api/v1/valuestreams').as('getValueStreams')
  cy.intercept('GET', '**/api/v1/organizations').as('getOrganizations')
  cy.visit(baseUrl, { timeout })
  cy.wait(['@getUsers', '@getTeams', '@getValueStreams', '@getOrganizations'])
})

Cypress.Commands.add('visitAdminPage', () => {
  cy.intercept('GET', '**/api/v1/users').as('getUsers')
  cy.intercept('GET', '**/api/v1/teams').as('getTeams')
  cy.intercept('GET', '**/api/v1/valuestreams').as('getValueStreams')
  cy.intercept('GET', '**/api/v1/organizations').as('getOrganizations')
  cy.intercept('GET', '**/api/v1/ticketboards').as('getBoards')
  cy.intercept('GET', '**/api/v1/repositories').as('getRepos')
  cy.intercept('GET', '**/api/v1/pipelines').as(
    'getPipelines',
  )
  cy.visit(`${baseUrl}/admin`, { timeout })
  cy.wait(
    [
      '@getUsers',
      '@getTeams',
      '@getValueStreams',
      '@getOrganizations',
      '@getBoards',
      '@getRepos',
      '@getPipelines',
    ],
    { timeout },
  )
})

Cypress.Commands.add('visitReportsPage', () => {
  cy.intercept('GET', '**/api/v1/users').as('getUsers')
  cy.intercept('GET', '**/api/v1/teams').as('getTeams')
  cy.intercept('GET', '**/api/v1/valuestreams').as('getValueStreams')
  cy.intercept('GET', '**/api/v1/organizations').as('getOrganizations')
  cy.intercept('GET', '**/api/v1/ticketboards').as('getBoards')
  cy.intercept('GET', '**/api/v1/repositories').as('getRepos')
  cy.intercept('GET', '**/api/v1/pipelines').as(
    'getPipelines',
  )
  cy.visit(`${baseUrl}/reports`, { timeout })
  cy.wait(
    [
      '@getUsers',
      '@getTeams',
      '@getValueStreams',
      '@getOrganizations',
      '@getBoards',
      '@getRepos',
      '@getPipelines',
    ],
    { timeout },
  )
})

Cypress.Commands.add('waitForAPIDataAfterUserChange', () => {
  cy.intercept('GET', '**/api/v1/users').as('getUsers')
  cy.intercept('GET', '**/api/v1/teams').as('getTeams')
  cy.intercept('GET', '**/api/v1/valuestreams').as('getValueStreams')
  cy.intercept('GET', '**/api/v1/organizations').as('getOrganizations')
  cy.intercept('GET', '**/api/v1/ticketboards').as('getBoards')
  cy.intercept('GET', '**/api/v1/repositories').as('getRepos')
  cy.intercept('GET', '**/api/v1/pipelines').as(
    'getPipelines',
  )
  cy.wait(
    [
      '@getUsers',
      '@getTeams',
      '@getValueStreams',
      '@getOrganizations',
      '@getBoards',
      '@getRepos',
      '@getPipelines',
    ],
    { timeout },
  )
})

Cypress.Commands.add('visitAddTeamPage', () => {
  cy.visitAdminPage()
  cy.get(`[aria-label="Add a Team"]`).click()
})

Cypress.Commands.add('pickOptionMUIAutocomplete', selector => {
  cy.get(selector).click({ force: true })
  // select the first item in the autocomplete
  // and make sure options exist otherwise the tests will fail
  cy.get(`li[data-option-index="0"]`).should('exist')
  cy.get(selector).blur()
  cy.get(selector).click({ force: true })
  cy.get(`li[data-option-index="0"]`).click({ force: true })
})
