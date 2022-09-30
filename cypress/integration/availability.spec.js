const reactComponentUpdateTimeout = 10000
// describe to only test in dev mode

function randomString(strLen) {
  return Math.round(36 ** (strLen + 1) - Math.random() * 36 ** strLen)
    .toString(36)
    .slice(1)
}

function mockAuth() {
  if (Cypress.config('mode') == 'pipeline') {
    cy.intercept('*', req => {
      req.headers.authorization = Cypress.env('TOKEN')
    })
  }
}

describe('Test page availability', () => {
  beforeEach(mockAuth)

  const screenshotFolderName = 'test_page_availability'

  it('can reach the frontend', () => {
    cy.visitDashboard()
    cy.get(`[aria-label='Holocron Logo']`).should('be.visible')
    cy.screenshot(`${screenshotFolderName}/can_reach_the_frontend`)
  })
})
