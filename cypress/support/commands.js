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

const timeout = 240000

cy.utils = {
  randomName: strLen =>
    `cypress-${Math.round(36 ** (strLen + 1) - Math.random() * 36 ** strLen)
      .toString(36)
      .slice(1)}`,
}

Cypress.Commands.add('mockAuth', () => {
  cy.intercept('*', req => {
    req.headers.authorization = Cypress.env('token')
  })
})

Cypress.Commands.add('visitAPI', () => {
  cy.visit('/api/v2', { timeout })
})

Cypress.Commands.add(
  'apiCreateOrganization',
  body =>
    cy.request({
      method: 'POST',
      url: `/api/v2/organizations`,
      body,
      headers: {
        'Content-Type': 'application/json',
        Authorization: Cypress.env('token'),
      },
    }),
)

Cypress.Commands.add(
  'apiDeleteOrganization',
  organizationId =>
    cy.request({
      method: 'DELETE',
      url: `/api/v2/organizations/${organizationId}`,
      headers: {
        Authorization: Cypress.env('token'),
      },
    }),
)

Cypress.Commands.add(
  'apiCreateValueStream',
  body =>
    cy.request({
      method: 'POST',
      url: `/api/v2/valuestreams`,
      body,
      headers: {
        'Content-Type': 'application/json',
        Authorization: Cypress.env('token'),
      },
    }),
)

Cypress.Commands.add(
  'apiDeleteValueStream',
  valueStreamId =>
    cy.request({
      method: 'DELETE',
      url: `/api/v2/valuestreams/${valueStreamId}`,
      headers: {
        Authorization: Cypress.env('token'),
      },
    }),
)


Cypress.Commands.add(
  'apiCreateTeam',
  body =>
    cy.request({
      method: 'POST',
      url: `/api/v2/teams`,
      body,
      headers: {
        'Content-Type': 'application/json',
        Authorization: Cypress.env('token'),
      },
    }),
)

Cypress.Commands.add(
  'apiUpdateTeam',
  (teamId, body) =>
    cy.request({
      method: 'PUT',
      url: `/api/v2/teams/${teamId}`,
      body,
      headers: {
        'Content-Type': 'application/json',
        Authorization: Cypress.env('token'),
      },
    }),
)

Cypress.Commands.add(
  'apiDeleteTeam',
  teamId =>
    cy.request({
      method: 'DELETE',
      url: `/api/v2/teams/${teamId}`,
      headers: {
        Authorization: Cypress.env('token'),
      },
    }),
)

Cypress.Commands.add('apiCreateMockUser', () => {
  cy.request({
    url: '/api/v2',
    headers: {
      Authorization: Cypress.env('token'),
    },
  })
},
)


Cypress.on('uncaught:exception', (err, runnable) => {
  // returning false here prevents Cypress from
  // failing the test in case anything
  // errors in the application for example
  // window.onload when visiting the page.
  return false
})