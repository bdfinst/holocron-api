describe('Test page availability', () => {
  beforeEach(cy.mockAuth)

  const screenshotFolderName = 'test_page_availability'

  it('can reach the frontend', () => {
    cy.visitDashboard()
    cy.get(`[aria-label='Holocron Logo']`).should('be.visible')
    cy.screenshot(`${screenshotFolderName}/can_reach_the_frontend`)
  })
})
