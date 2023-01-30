const screenshotFolderName = 'test_report'

const confirmNoCrashesFound = () => {
  // click away from focus
  cy.get('body').click(0, 0)
  cy.get(`[aria-label="Agile Board Report Title"]`).should('be.visible')
}

const filterByUrl = () => {
  cy.get(`[aria-label="Filter url"]`).click({ force: true })
  cy.get(`[aria-label="Search a Board Url"]`).type(`1`)
  cy.screenshot(`${screenshotFolderName}/can_filter_by_team_id`)
  confirmNoCrashesFound()
}

const filterByName = () => {
  // filter by name
  cy.get(`[aria-label="Filter name"]`).click({ force: true })
  cy.get(`[aria-label="Search a Name"]`).type(`a`)
  cy.screenshot(`${screenshotFolderName}/can_filter_by_name`)
  confirmNoCrashesFound()
}

const filterByBoardStatus = () => {
  // filter by onboarding status
  cy.get(`[aria-label="Filter used"]`).click({ force: true })
  // select onboarded first
  cy.get(`[aria-label="Select Board Status"]`)
    .parent()
    .click()
    .get('ul > li[data-value="true"]')
    .click()
  cy.screenshot(`${screenshotFolderName}/can_filter_by_status_onboarded`)
  // select not onboarded
  cy.get('[aria-label="Select Board Status"]')
    .parent()
    .click()
    .get('ul > li[data-value="false"]')
    .click()
  cy.screenshot(`${screenshotFolderName}/can_filter_by_status_not_onboarded`)
  // // select all
  cy.get('[aria-label="Select Board Status"]')
    .parent()
    .click()
    .get('ul > li[data-value=""]')
    .click()
  cy.screenshot(`${screenshotFolderName}/can_filter_by_status_all`)
  confirmNoCrashesFound()
}

describe('Test Report', () => {
  beforeEach(cy.mockAuth)

  it('should allow us to filter the boards by teamId, name, and onboarding status', () => {
    // filter by teamId
    cy.visitReportsPage()
    confirmNoCrashesFound()
    filterByUrl()
    filterByName()
    filterByBoardStatus()
  })
})
