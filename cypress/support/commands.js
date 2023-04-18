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

const apiV1Url = `${Cypress.config('baseUrl')}/api/v1`
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

Cypress.Commands.add('visitAPI', () => {
  cy.visit(apiV1Url, { timeout })
})
