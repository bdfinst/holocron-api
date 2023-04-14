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

cy.utils = {
  randomName: strLen =>
    `cypress-${Math.round(36 ** (strLen + 1) - Math.random() * 36 ** strLen)
      .toString(36)
      .slice(1)}`,
}

Cypress.Commands.add('mockAuth', () => {
  if (Cypress.config('mode') == 'pipeline') {
    cy.intercept('*', req => {
      req.headers.authorization = Cypress.env('TOKEN')
    })
  }
})

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
  cy.visit(`${baseUrl}/admin`, { timeout })
  cy.wait(['@getUsers', '@getTeams', '@getValueStreams', '@getOrganizations'], {
    timeout,
  })
})

Cypress.Commands.add('visitReportsPage', () => {
  cy.intercept('GET', '**/api/v1/users').as('getUsers')
  cy.intercept('GET', '**/api/v1/teams').as('getTeams')
  cy.intercept('GET', '**/api/v1/valuestreams').as('getValueStreams')
  cy.intercept('GET', '**/api/v1/organizations').as('getOrganizations')
  cy.intercept('GET', '**/api/v1/ticketboards').as('getBoards')
  cy.intercept('GET', '**/api/v1/repositories').as('getRepos')
  cy.intercept('GET', '**/api/v1/pipelines').as('getPipelines')
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

Cypress.Commands.add('waitForCollectorTargets', () => {
  cy.intercept('GET', '**/api/v1/ticketboards').as('getBoards')
  cy.intercept('GET', '**/api/v1/repositories').as('getRepos')
  cy.intercept('GET', '**/api/v1/pipelines').as('getPipelines')
  cy.wait(['@getBoards', '@getRepos', '@getPipelines'], { timeout })
})

Cypress.Commands.add('visitAddTeamPage', () => {
  cy.intercept('GET', '**/api/v1/users').as('getUsers')
  cy.intercept('GET', '**/api/v1/teams').as('getTeams')
  cy.intercept('GET', '**/api/v1/valuestreams').as('getValueStreams')
  cy.intercept('GET', '**/api/v1/organizations').as('getOrganizations')
  cy.intercept('GET', '**/api/v1/ticketboards').as('getBoards')
  cy.intercept('GET', '**/api/v1/repositories').as('getRepos')
  cy.intercept('GET', '**/api/v1/pipelines').as('getPipelines')
  cy.visit(`${baseUrl}/admin/add-team`, { timeout })
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

Cypress.Commands.add('visitUpdateTeamPage', teamName => {
  cy.intercept('GET', '**/api/v1/users').as('getUsers')
  cy.intercept('GET', '**/api/v1/teams').as('getTeams')
  cy.intercept('GET', '**/api/v1/valuestreams').as('getValueStreams')
  cy.intercept('GET', '**/api/v1/organizations').as('getOrganizations')
  cy.intercept('GET', '**/api/v1/ticketboards').as('getBoards')
  cy.intercept('GET', '**/api/v1/repositories').as('getRepos')
  cy.intercept('GET', '**/api/v1/pipelines').as('getPipelines')
  cy.visitAdminPage()
  cy.get('[aria-label="Search team by name"]').type(teamName)
  cy.get(`[aria-label="update-team-${teamName}"]`).click()
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
  cy.wait(['@getUsers', '@getTeams', '@getValueStreams', '@getOrganizations'], {
    timeout,
  })
})

Cypress.Commands.add('pickOptionMUIAutocomplete', selector => {
  // select the first item in the autocomplete
  // and make sure options exist otherwise the tests will fail
  cy.get(selector).click({ force: true })
  cy.get(`li[data-option-index="0"]`).click({ force: true })
})
